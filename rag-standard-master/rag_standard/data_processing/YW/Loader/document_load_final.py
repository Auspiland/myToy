import os, json, time, sys, re, requests
from . import load_excel, load_pdf, load_ppt, load_docx, load_hwp, load_hwpx, load_upstageapi_pdf
from .Parsing import chunk_by_page, chunk_by_token

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting

global log
log = setup_logger.setup_logger('DocumentLoad', 'document_load')
config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
config = config_setting.load_yaml_config(config_path)

config_setting.load_env()

##### 확장자별로 필요한 클래스 호출
loadexcel = load_excel.LoadExcel()
loadpdf = load_pdf.LoadPDF()
loadppt = load_ppt.LoadPPT()
loaddocx = load_docx.LoadDOCX()
loadhwp = load_hwp.LoadHWP()
loadhwpx = load_hwpx.LoadHWPX()
upstage = load_upstageapi_pdf.UPSTAGE()

##### 토큰으로 청크 구분할 거라면 이 클래스 호출
w_token = chunk_by_token.CHUNK_W_TOKEN()

def count_tokens(text):
    result = requests.post(
        url='http://172.16.16.192:29034/tokenize', 
        json={
            'model': "qwen-2.5", 
            "messages": [
                {"role": "user", "content": text}
                ]
            }
        )

    token_len = json.loads(result.text)['count']

    return token_len

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

def clean_cid(text):
    """ 정규식으로 텍스트 정제 """
    return re.sub(r"\(cid:\d+\)", "", text).strip()

class LoadData:
    """ load_all만 호출하면 됨 <- load_data로 일반 문서 로드 방식이 필요한 경우 활용됨 """
    def __init__(self):
        pass

    def load_all(self, pname=config['data_processing_settings']['version_name'], root_path=config['data_processing_settings']['root_path'], file_path=config['data_processing_settings']['file_path'], page=config['data_processing_settings']['page_tf'], token=config['data_processing_settings']['token_tf'], api=config['data_processing_settings']['api_tf']):
        """
        파일을 로드하고 청크 단위로 분할하여 메타데이터를 생성하는 메인 함수
        
        Args:
            pname (str): 결과물이 저장될 최상위 폴더 이름 (사용자가 지정하는 버전명, 한 번 돌릴 때마다 지정한 이 이름으로 폴더 생성돼서 결과 저장됨)
            root_path (str): 결과물이 저장될 최상위 폴더의 저장 위치 (pname이 저장될 위치/경로) - ex. /data/aisvc_data/RAG/Rag_Standard_v2/data
            file_path (str): 처리할 파일 경로나 폴더 경로 (원본 파일이 저장되어 있는 폴더 경로)
            page (bool): 페이지로 chunking할 건지 여부
            token (bool): token으로 chunking할 건지 여부
            api (bool): Upstage API를 호출할 건지 여부
            
        Returns:
            결과는 파일로 저장
        """
        process_start_time = time.time()
        mid_path = f"{root_path}/{pname}/Interim" # 중간결과물을 저장할 폴더 경로
        save_path = f"{root_path}/{pname}/Split" # 최종결과물을 저장할 폴더 경로
        os.makedirs(mid_path, exist_ok=True)
        os.makedirs(save_path, exist_ok=True)

        # 파일 목록 생성
        file_paths = []
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                # 제외할 디렉토리 목록 설정
                exclude_dirs = ['.ipynb_checkpoints']
                
                # exclude_dirs에 포함된 디렉토리들을 dirs(현재 검색중인 디렉토리 목록)에서 제외
                for d in exclude_dirs:
                    if d in dirs:
                        dirs.remove(d)
                        
                for file in files:
                    # .ipynb_checkpoints 파일은 제외하고 나머지 파일들의 전체 경로를 리스트에 추가
                    if file != '.ipynb_checkpoints':
                        file_paths.append(os.path.join(root, file))
        else:
            # file_path가 디렉토리가 아닌 경우 단일 파일로 처리
            file_paths.append(file_path)

        page_tf = to_boolean(page)
        token_tf = to_boolean(token)
        api_tf = to_boolean(api)
        
        for file in file_paths:
            file_name_without_ext, extension = os.path.basename(file).rsplit('.', 1) # 파일명과 확장자 분리
            if api_tf and extension.lower() == 'pdf':
                # Upstage API 호출
                file_name, extension, modified, created, only_text_content, text_table_content, total_w_table = upstage.preprocess_api(file, pname, mid_path, root_path, os.getenv("UPSTAGE_API_KEY"))
                log.info(f"Loaded Upstage API metadata saved")
            else:
                # 일반 문서 로드 방식 호출
                file_name, extension, modified, created, only_text_content, text_table_content, total_w_table = self.load_data(file, mid_path)
                
                fname, chunks = chunk_by_page.page_chunk(file_name, only_text_content, text_table_content)
                
                for chunk_index, (chunk, content) in enumerate(chunks.items()):
                    retrieve_content = only_text_content.get(chunk, "")
                    
                docu_load_path = f"{root_path}/{pname}/Loader/Document"
                os.makedirs(docu_load_path, exist_ok=True)

                # 기존 JSON 파일이 있으면 불러오기, 없으면 빈 리스트로 시작
                if os.path.exists(f"{docu_load_path}/{file_name_without_ext}.json"):
                    with open(f"{docu_load_path}/{file_name_without_ext}.json", "r", encoding="utf-8-sig") as f:
                        try:
                            existing_data = json.load(f)  # 기존 데이터 불러오기
                            if not isinstance(existing_data, list):  
                                existing_data = [existing_data]  # 기존 데이터가 리스트가 아닐 경우 리스트로 변환
                        except json.JSONDecodeError:
                            existing_data = []  # JSON 파일이 비어 있거나 손상된 경우 빈 리스트로 초기화
                else:
                    existing_data = []  # 파일이 없으면 빈 리스트로 시작
    
                # 현재 청크에 대한 메타데이터 항목 생성
                meta_entry = {
                    'project_name': pname,
                    'file_name': fname,
                    'extension': extension,
                    'chunk_order': str(chunk_index + 1),
                    'chunk_name': chunk,
                    'file_modified': modified,
                    'file_created': created,
                    'filtering_id': fname + '_' + chunk,
                    'llm_content': clean_cid(content.lower()),
                    'retrieve_content': clean_cid(retrieve_content.lower()),
                    'llm_token_count': count_tokens(clean_cid(content.lower())),
                    'retrieve_token_count': count_tokens(clean_cid(retrieve_content.lower())),
                    'file_size': int(os.path.getsize(file))
                }
    
                existing_data.append(meta_entry)  # 리스트에 추가
                
                with open(f'{docu_load_path}/{file_name_without_ext}.json', "w", encoding="utf-8-sig") as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
                log.info(f"Loaded Document Loader metadata saved at {docu_load_path}")
    
            if page_tf:
                # 페이지 단위 청크 생성: fname, chunks는 {청크명: 내용} 형식
                fname, chunks = chunk_by_page.page_chunk(file_name, only_text_content, text_table_content)
            elif token_tf:
                # 토큰 단위 청크 생성: fname, llm, retrieve는 각각 {청크명: 내용} 형식
                fname, llm, retrieve = w_token.process_json(file, total_w_table, max_tokens=config['upstage_api_settings']['max_tokens'], overlap_tokens=config['upstage_api_settings']['overlap_tokens'], token_limit=config['upstage_api_settings']['token_limit'], separators=[r"<table[^>]*", r"\n\n"])
            else:
                log.error("[ERROR] How do you want to parse the data - by page or token?")
                print(f"Error occured with {file_name} ({extension})")
    
            # mode에 따라 처리할 딕셔너리 선택 (page: chunks, token: llm)
            if page_tf:
                chunk_dict = chunks
            elif token_tf:
                chunk_dict = llm
        
            # 각 청크별로 메타데이터 생성
            for chunk_index, (chunk, content) in enumerate(chunk_dict.items()):
                # token 모드에서는 별도의 retrieve 딕셔너리에서 가져오고, page 모드에서는 only_text_content에서 보완
                if token_tf:
                    retrieve_content = retrieve.get(chunk, "")
                else:
                    retrieve_content = only_text_content.get(chunk, "")

                if api_tf and page_tf:
                    save_file = os.path.join(save_path, f"API_PAGE/{fname}.json")
                elif api_tf and token_tf:
                    save_file = os.path.join(save_path, f"API_TOKEN/{fname}.json")
                elif not api_tf and page_tf:
                    save_file = os.path.join(save_path, f"DOCU_PAGE/{fname}.json")
                elif not api_tf and token_tf:
                    save_file = os.path.join(save_path, f"DOCU_TOKEN/{fname}.json")
                else:
                    log.error("[ERROR] No directory made - Check the boolean value of api, page, and token")
                    save_file = None

                if save_file:
                    os.makedirs(os.path.dirname(save_file), exist_ok=True)
                
                # 기존 JSON 파일이 있으면 불러오기, 없으면 빈 리스트로 시작
                if os.path.exists(save_file):
                    with open(save_file, "r", encoding="utf-8-sig") as f:
                        try:
                            existing_data = json.load(f)  # 기존 데이터 불러오기
                            if not isinstance(existing_data, list):  
                                existing_data = [existing_data]  # 기존 데이터가 리스트가 아닐 경우 리스트로 변환
                        except json.JSONDecodeError:
                            existing_data = []  # JSON 파일이 비어 있거나 손상된 경우 빈 리스트로 초기화
                else:
                    existing_data = []  # 파일이 없으면 빈 리스트로 시작
    
                # 현재 청크에 대한 메타데이터 항목 생성
                meta_entry = {
                    'project_name': pname,
                    'file_name': fname,
                    'extension': extension,
                    'chunk_order': str(chunk_index + 1),
                    'chunk_name': chunk,
                    'file_modified': modified,
                    'file_created': created,
                    'filtering_id': fname + '_' + chunk,
                    'llm_content': clean_cid(content.lower()),
                    'retrieve_content': clean_cid(retrieve_content.lower()),
                    'llm_token_count': count_tokens(clean_cid(content.lower())),
                    'retrieve_token_count': count_tokens(clean_cid(retrieve_content.lower())),
                    'file_size': int(os.path.getsize(file))
                }
    
                existing_data.append(meta_entry)  # 리스트에 추가
                
                # 메타데이터를 JSON 파일로 저장 (덮어씌우지 않고 누적 저장)
                with open(save_file, "w", encoding="utf-8-sig") as f:
                    json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
                log.info(f"Splitted metadata saved at {save_file}")

        # 총 처리 시간 계산 및 로깅
        process_time = time.time() - process_start_time
        log.info("Overall time taken for loading: %.2f seconds", process_time)
    
    def load_data(self, fpath, mid_path):
        """
        파일의 확장자를 확인하여 적절한 로더를 실행하는 함수
        - PPT: ppt, pptx
        - EXCEL: xlsx, xls, xlsm
        - PDF: pdf
        - WORD: docx
        - 한글: hwp, hwpx
        """
        # 파일명과 확장자 분리 (예: 'test.pdf' -> 'test', 'pdf')
        _, extension = os.path.basename(fpath).rsplit('.', 1)

        # 파일 확장자에 따라 적절한 로더 함수 호출
        if extension.lower() in ['ppt', 'pptx']: # PPT 파일 처리
            return loadppt.load_ppt(fpath)
        elif extension.lower() in ['xlsx', 'xls', 'xlsm']: # 엑셀 파일 처리
            return loadexcel.load_excel(fpath, mid_path)
        elif extension.lower() in ['pdf']: # PDF 파일 처리
            return loadpdf.load_pdf(fpath)
        elif extension.lower() in ['docx']: # Word 문서 처리
            return loaddocx.load_docx(fpath)
        elif extension.lower() in ['hwp']: # 한글 문서(hwp 형식) 처리
            return loadhwp.load_hwp(fpath)
        elif extension.lower() in ['hwpx']:
            return loadhwpx.load_hwpx(fpath, mid_path)
        else:
            log.info(f'{fpath}의 {extension}은 지원하지 않는 파일형식입니다. EXCEL, PPT, PDF, DOCX, HWP인지 다시 확인해주세요.')

if __name__ == '__main__':
    pname = config['data_processing_settings']['version_name']
    root_path = config['data_processing_settings']['root_path']
    file_path = config['data_processing_settings']['file_path']
    mid_path = f"{root_path}/{pname}/Interim"
    save_path = f"{root_path}/{pname}/Split"
    page = config['data_processing_settings']['page_tf']
    token = config['data_processing_settings']['token_tf']
    api = config['data_processing_settings']['api_tf']

    # 호출된 정보들 확인
    print(f"Project Name: {pname}\nRoot path: {root_path}\nFile path: {file_path}\nIn-progress result path: {mid_path}\nTarget path: {save_path}\nWhether chunk by page: {page_tf}\nWhether chunk by token: {token_tf}\nWhether use Upstage API: {api_tf}")

    # 파일 로드하는 함수 호출 (로그 찍히며 작업 수행됨)
    LoadData().load_all(pname, root_path, file_path, page=page_tf, token=token_tf, api=api_tf)