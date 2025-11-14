# -*- coding: utf-8 -*-
import os, sys, time, traceback, json
from setproctitle import setproctitle
from tqdm import tqdm

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # 상대경로로 root 설정
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting

from rag_standard.data_processing.YW.Loader.document_load_final import LoadData
from rag_standard.data_processing.YW.Embedding.embedding_final import calculate_embed
from rag_standard.data_processing.YW.Embedding.qdrant_final import QdrantHelper
from rag_standard.data_processing.YW.Embedding.opensearch_final import OpenSearchHelper

setproctitle("YewonLee/nlp/Pipeline")

def to_boolean(value):
    """ 문자열을 boolean 값으로 변환하는 함수 """
    # 이미 불리언이면 그대로 반환
    if isinstance(value, bool):
        return value
    # 문자열인 경우, 소문자로 변환한 후 True에 해당하는 값이면 True 반환
    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ['true', '1', 't', 'yes', 'y']:
            return True
        elif value_lower in ['false', '0', 'f', 'no', 'n']:
            return False
        else:
            raise ValueError(f"불리언으로 변환할 수 없는 문자열: {value}")
    # 기타 자료형은 내장 bool() 함수를 사용해 변환
    return bool(value)

class Pipeline:
    """Complete RAG pipeline from document loading to vector storage"""
    
    def __init__(self):
        """Initialize the pipeline with configuration and helpers"""
        self.log = setup_logger.setup_logger('Pipeline', 'pipeline')
        
        config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
        self.config = config_setting.load_yaml_config(config_path)
        
        # Initialize helpers
        self.loader = LoadData()
        self.qdrant = QdrantHelper()
        self.opensearch = OpenSearchHelper()
        
        # Set paths
        self.version_name = self.config['data_processing_settings']['version_name']
        self.root_path = self.config['data_processing_settings']['root_path']
        self.file_path = self.config['data_processing_settings']['file_path']
        
        # Set flags
        self.page_tf = self.config['data_processing_settings']['page_tf']
        self.page_tf = to_boolean(self.page_tf)
        self.token_tf = self.config['data_processing_settings']['token_tf']
        self.token_tf = to_boolean(self.token_tf)
        self.api_tf = self.config['data_processing_settings']['api_tf']
        self.api_tf = to_boolean(self.api_tf)
        self.qdrant_tf = self.config['data_processing_settings']['qdrant_tf']
        self.qdrant_tf = to_boolean(self.qdrant_tf)
        
        # Create necessary directories
        self._create_directories()
        
    def _create_directories(self):
        """Create necessary directories for the pipeline"""
        directories = [
            f"{self.root_path}/{self.version_name}/Interim",
            f"{self.root_path}/{self.version_name}/Split",
            f"{self.root_path}/{self.version_name}/Loader",
            f"{self.root_path}/{self.version_name}/Embedding"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.log.info(f"Created directory: {directory}")
    
    def _load_documents(self):
        """Load and process documents"""
        try:
            self.log.info("Starting document loading process...")
            self.loader.load_all(
                pname=self.version_name,
                root_path=self.root_path,
                file_path=self.file_path,
                page=self.page_tf,
                token=self.token_tf,
                api=self.api_tf
            )
            self.log.info("Document loading completed successfully")
            return True
        except Exception as e:
            self.log.error(f"Error in document loading: {traceback.format_exc()}")
            return False
    
    def _process_embeddings(self):
        """Process embeddings for loaded documents"""
        try:
            self.log.info("Starting embedding process...")
            
            # Get the appropriate prefix based on processing type
            prefix = "API" if self.api_tf else "DOCU"
                
            # Process both page and token based chunks if enabled
            if self.page_tf:
                base_dir = f"{self.root_path}/{self.version_name}/Split/{prefix}_PAGE"
                self._process_chunk_type(base_dir, "PAGE")

            if self.token_tf:
                base_dir = f"{self.root_path}/{self.version_name}/Split/{prefix}_TOKEN"
                self._process_chunk_type(base_dir, "TOKEN")
                
            self.log.info("Embedding process completed successfully")
            return True
        except Exception as e:
            self.log.error(f"Error in embedding process: {traceback.format_exc()}")
            return False
    
    def _process_chunk_type(self, base_dir, chunk_type):
        """Process embeddings for a specific chunk type"""
        try:
            # Get the directory for this chunk type
            chunk_dir = f"{base_dir}"
            if not os.path.exists(chunk_dir):
                self.log.warning(f"Directory not found: {chunk_dir}")
                return
            
            # Process each file in the directory
            for root, _, files in os.walk(chunk_dir):
                for file in tqdm(files, desc=f"Processing {chunk_type} chunks"):
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        
                        # Read metadata
                        with open(file_path, 'r', encoding='utf-8-sig') as f:
                            metadata = json.load(f)
                        
                        # Calculate embeddings
                        enriched_metadata = calculate_embed(metadata, qdrant_tf=self.qdrant_tf)
                        
                        if not enriched_metadata:
                            self.log.warning(f"No embeddings generated for {file}")
                            continue
                        
                        # Save enriched metadata
                        save_dir = f"{self.root_path}/{self.version_name}/Embedding"
                        if self.qdrant_tf:
                            save_path = f"{save_dir}/Qdrant/{file}"
                        else:
                            save_path = f"{save_dir}/OpenSearch/{file}"
                            
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        with open(save_path, 'w', encoding='utf-8-sig') as f:
                            json.dump(enriched_metadata, f, ensure_ascii=False, indent=2)
                            
                        self.log.info(f"Processed and saved embeddings for {file}")
                        
        except Exception as e:
            self.log.error(f"Error processing {chunk_type} chunks: {traceback.format_exc()}")
            raise
    
    def run(self):
        """Run the complete pipeline"""
        start_time = time.time()
        self.log.info("Starting RAG pipeline...")
        
        try:
            # Step 1: Load documents
            if not self._load_documents():
                self.log.error("Document loading failed. Stopping pipeline.")
                return False
            
            # Step 2: Process embeddings
            if not self._process_embeddings():
                self.log.error("Embedding process failed. Stopping pipeline.")
                return False
            
            # Calculate and log total processing time
            total_time = time.time() - start_time
            self.log.info(f"Pipeline completed successfully in {total_time:.2f} seconds")
            return True
            
        except Exception as e:
            self.log.error(f"Pipeline failed: {traceback.format_exc()}")
            return False

def main():
    """Main entry point for the pipeline"""
    pipeline = Pipeline()
    success = pipeline.run()
    
    if success:
        print("Pipeline completed successfully!")
    else:
        print("Pipeline failed. Check the logs for details.")

if __name__ == "__main__":
    main() 