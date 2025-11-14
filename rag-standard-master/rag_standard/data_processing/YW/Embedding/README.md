# Embedding Module

A comprehensive embedding system that processes document chunks and stores them in vector databases (Qdrant and OpenSearch) for efficient retrieval in RAG (Retrieval-Augmented Generation) applications.

## Features

- **Dual Vector Storage**: Supports both Qdrant and OpenSearch vector databases
- **Hybrid Embedding**: Generates both dense and sparse vectors for each document chunk
  - Dense vectors using BGE model via API
  - Sparse vectors using BM25 with Korean language support
- **Korean Language Support**: 
  - Uses Kiwi for Korean text tokenization
  - Supports custom dictionaries for domain-specific terms
- **Version Control**: Maintains document versions in vector databases
- **Metadata Preservation**: Stores comprehensive metadata with each vector

## Project Structure

```
Embedding/
├── embedding_final.py     # Main embedding implementation
├── qdrant_final.py        # Qdrant vector database integration
├── opensearch_final.py    # OpenSearch vector database integration
├── Embedding 실행.ipynb    # Example notebook
└── logs/                  # Log files directory
```

## Configuration

The system uses configuration parameters from multiple sources:

1. From `configs/main_config.yaml`:
```yaml
# --- Metadata Settings ---
data_processing_settings:
  version_name: "string"       # Version identifier
  root_path: "string"          # Root directory path
  qdrant_tf: "boolean"         # Enable Qdrant storage

# --- Database Settings ---
db_settings:
  opensearch_index: "string"   # OpenSearch index name
  qdrant_host: "string"        # Qdrant host
  qdrant_port: "string"        # Qdrant port
  qdrant_collection: "string"  # Qdrant collection name
```

2. From `.env` file:
```env
# === 모델 API 정보 ===
TEXT_EMBEDDING_API_URL=http://<EMBEDDING_API_HOST>:<EMBEDDING_API_PORT>/embed  # BGE embedding API endpoint

# === OpenSearch 접속 정보 ===
OPENSEARCH_HOST=<YOUR_OPENSEARCH_HOST>
OPENSEARCH_PORT=<YOUR_OPENSEARCH_PORT>
```

3. From `configs/naive_rag_workflow.yaml`:
```yaml
tokenizer:
  dictionary_path: "string"    # Path to Kiwi custom dictionary
```

## Usage

1. Configure the settings in all three files:
   - `configs/main_config.yaml`
   - `.env` (refer to the template)
   - `configs/naive_rag_workflow.yaml`
2. Run the embedding system:

```python
from embedding_final import main

# Run the embedding process
main()
```

## Vector Database Integration

### Qdrant

- Supports both dense and sparse vectors
- Uses cosine similarity for vector search
- Maintains document versions
- Stores comprehensive metadata
- Handles vector storage in format: `{"indices": [...], "values": [...]}`

### OpenSearch

- Implements HNSW algorithm for approximate nearest neighbor search
- Uses custom lowercase analyzer for text fields
- Supports Korean language processing
- Stores both dense vectors and tokenized text
- Uses text_sparse_kiwi for sparse vector storage

## Output Structure

The system generates the following outputs:

```
version_name/
└── Embedding/
    ├── Qdrant/
    │   └── {file_name}.json    # Qdrant metadata and vectors
    └── OpenSearch/
        └── {file_name}.json    # OpenSearch metadata and vectors
```

## Dependencies

- requests: For API calls
- qdrant-client: For Qdrant integration
- opensearch-py: For OpenSearch integration
- kiwipiepy: For Korean text tokenization
- fastembed: For BM25 sparse embeddings
- tqdm: For progress tracking
- setproctitle: For process naming

## Logging

The system maintains detailed logs in the `logs` directory:
- Log files are limited to 5MB each
- Up to 10 backup log files are maintained
- Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Separate log files for Embedding, Qdrant, and OpenSearch operations

## Notes

- The system automatically handles file encoding and special characters
- Supports both single file and directory processing
- Excludes empty documents (zero token count)
- Maintains version history for updated documents
- Uses MD5 hashing for generating unique document IDs
- Supports custom Korean dictionaries for domain-specific terms
- Handles API timeouts with extended timeout period (999999 seconds)
- Processes documents in batches for efficient embedding generation 