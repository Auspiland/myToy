# library import
import re, os, sys
from tokenizers import Tokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger

global log
log = setup_logger.setup_logger('ChunkByToken', 'chunk_by_token')

# tokenizer
tokenizer_pro = Tokenizer.from_pretrained("upstage/solar-pro-tokenizer")
tokenizer_mini = Tokenizer.from_pretrained("upstage/solar-1-mini-tokenizer")

def initialize_tokenizer():
    """
    Solar 토크나이저를 초기화하고 토큰 수 계산 함수를 반환

    Returns:
        tuple: (solar_token_len_pro, solar_token_len_mini)
            - solar_token_len_pro: solar-pro 토크나이저로 토큰 수를 계산하는 함수
            - solar_token_len_mini: solar-mini 토크나이저로 토큰 수를 계산하는 함수
    """
    # from tokenizers import Tokenizer
    try:
        def solar_token_len_pro(text):
            """ 토큰 수 반환 함수
            solar-pro-tokenizer : solar-pro"""
            tokens = tokenizer_pro.encode(text)
            return len(tokens.ids)
    
        def solar_token_len_mini(text):
            """ 토큰 수 반환 함수
            solar-1-mini-tokenizer : embedding-query, embedding-passage"""
            tokens = tokenizer_mini.encode(text)
            return len(tokens.ids)

        return solar_token_len_pro, solar_token_len_mini

    except Exception as e:
        log.error("Tokenizer Initialization Error: %s", e)
        return None, None

def initialize_text_splitter(token_length_function, max_tokens=2000, overlap_tokens=300, separators=[r"<table[^>]*", r"\n\n"]):
    """
    chunk 분할에 사용할 RecursiveCharacterTextSplitter 초기화하여 반환

    Args:
        token_length_function (function): 토큰 길이를 계산하는 함수
        max_tokens (int): 최대 토큰 길이
        overlap_tokens (int): 오버랩 길이
        separators (list): 분할 구분자

    Return:
        - text_splitter : 테이블 요소와 줄바꿈을 기준으로 분할하는 TextSplitter를 초기화
    """
    try:
        # separators=["�", "\n\n"]
        # # separators=["\n\n"]
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=max_tokens,
            chunk_overlap=overlap_tokens,
            length_function=token_length_function,
            keep_separator=True, # separator 없애는 옵션
            is_separator_regex=True,
        )
        
        return text_splitter
        
    except Exception as e:
        log.error("TextSplitter Initialization Error: %s", e)
        return None

class CHUNK_W_TOKEN:
    """ process_json만 호출하면 됨 <- process_chunk_split으로 token으로 청크 생성하고 truncate_to_4000_tokens로 최종 검증 """
    def __init__(self):
        pass
    
    def process_json(self, fpath, total_w_table, max_tokens=2000, overlap_tokens=300, token_limit=3900, separators=[r"<table[^>]*>", r"\n\s*\|[\s:-]+\|\s*\n", r"\n\n"]):
        """
        입력된 텍스트를 처리하여 주어진 token 조건에 따라 분할된 청크를 반환

        Args:
            fpath (str): 처리하고 있는 파일의 경로
            total_w_table (str): 파일 문서의 내용을 전부 저장한 문자열 (테이블도 추출)
            max_tokens (int): 청크의 최대 토큰 길이 (default: 2000)
            overlap_tokens (int): 청크 오버랩 길이 (default: 300)
            token_limit (int): 청크의 상한선 - LLM에 넣을 때 토큰 수 초과되지 않기 위함 (default: 3900)
            separators (list): 청크 분할자 (default: [r"<table[^>]*", r"\n\n"])

        Returns:
            file_name_without_ext (str): 파일명
            Dict about llm_content: 주어진 토큰 조건에 따라 청크 분할한 결과 (텍스트+테이블)
            Dict about retrieve_content: 주어진 토큰 조건에 따라 청크 분할한 결과 (텍스트만)

        최종 결과물로 추출되는 llm_content, retrieve_content 딕셔너리 형식:
            {
                '페이지 번호': 페이지 내용,
                '페이지 번호': 페이지 내용,
                 ...
            }
        """
        file_name_without_ext, extension = os.path.basename(fpath).rsplit('.', 1)  # 파일 이름 # 확장자
        try:
            log.info("Processing JSON file: %s", fpath)
            
            # Step 1: Initialize tokenizer
            solar_token_len_pro, solar_token_len_mini = initialize_tokenizer()
            if not solar_token_len_pro or not solar_token_len_mini:
                log.error("Tokenizer initialization failed for %s", fpath)
                return None

            # Step 2: Initialize text splitter
            text_splitter = initialize_text_splitter(solar_token_len_mini, max_tokens=max_tokens, overlap_tokens=overlap_tokens, separators=separators)
            if not text_splitter:
                log.error("TextSplitter initialization failed for %s.", fpath)
                return None
            
            # Step 3: text splitter 적용하여 청크 생성
            # llm_content = data['metadata']['content']['llm_content']
            chunk_results = self.process_chunk_split(total_w_table, text_splitter, solar_token_len_pro, solar_token_len_mini, overlap_tokens=overlap_tokens, token_limit=token_limit)

            log.info("JSON file processed successfully: %s", fpath)
            return file_name_without_ext, {page: data["llm_content"] for page, data in chunk_results.items()}, {page: data["retrieve_content"] for page, data in chunk_results.items()}

        except Exception as e:
            log.error("Error processing JSON file %s: %s", fpath, e)
            return None
        
    def process_chunk_split(self, total_w_table, text_splitter, solar_token_len_pro, solar_token_len_mini, overlap_tokens=300, token_limit=3900):
        """
        LLM Chunk, Retrieve Chunk 생성
        - 전체 텍스트에서 청크를 생성하고, 각 청크의 토큰 수를 검증 및 조정하여 최종 결과 반환

        Args:
            total_w_table (str): 전체 테이블 데이터를 포함하는 텍스트
            text_splitter (function): 청크 분할을 위한 함수
            solar_token_len_pro (function): LLM 청크의 토큰 길이를 계산하는 함수
            solar_token_len_mini (function): Retrieve 청크의 토큰 길이를 계산하는 함수
            overlap_tokens (int, optional): 청크 병합 시 고려하는 최소 토큰 수 - 청크 오버랩 길이 (default: 300)
            token_limit (int, optional): 청크별 최대 토큰 수 제한 - LLM에 넣을 때 토큰 수 초과되지 않기 위함 (default: 3900)
        
        Returns:
            chunk_results (dict): 분할된 청크별로 LLM 내용과 Retrieve 내용, 그리고 각각의 토큰 수를 저장한 결과

        최종 결과물로 추출되는 chunk_results 딕셔너리 형식:
            {
                '청크 번호': {
                        "llm_content": LLM 처리용 텍스트,
                        "retrieve_content": 검색/리트리브용 텍스트,
                        "llm_token_count": LLM 텍스트의 토큰 수,
                        "retrieve_token_count": Retrieve 텍스트의 토큰 수
                    },
                '청크 번호': {
                        "llm_content": LLM 처리용 텍스트,
                        "retrieve_content": 검색/리트리브용 텍스트,
                        "llm_token_count": LLM 텍스트의 토큰 수,
                        "retrieve_token_count": Retrieve 텍스트의 토큰 수
                    },
                ...
            }
        """
        try:
            log.info("Processing chunk split...")
            llm_chunk, retrieve_chunk = [], []

            # 전체 텍스트(total_w_table)를 기반으로 청크 생성 (text_splitter를 이용)
            chunks = text_splitter.create_documents([total_w_table])

            for ch in chunks:
                try:
                    chunk = ch.page_content # 현재 청크의 콘텐츠 추출
                    # 청크 내에 <table> 태그가 포함되어 있으면 HTML 파싱 후 텍스트 추출
                    if re.search(r"<table", chunk) or re.search(r"</table>", chunk):
                        soup = BeautifulSoup(chunk, "html.parser")
                        plain_text = soup.get_text(separator=" ", strip=True)

                    # 마크다운 표 처리: 마크다운 형식의 표를 별도의 청크로 인식 (포맷은 그대로 유지)
                    # elif re.search(r'\n\s*\|[\s:-]+\|\s*\n', chunk):
                    #     plain_text = chunk
                        
                    else:
                        plain_text = chunk

                    # 추가 로직 : overlap_tokens 미만의 청크와 바로 앞 청크 병합 (합친 결과가 token_limit 미만일 때)
                    if retrieve_chunk and solar_token_len_mini(plain_text) < overlap_tokens:
                        previous_chunk = retrieve_chunk[-1] # 가장 최근에 들어간 청크
                        combined_length = solar_token_len_mini(previous_chunk) + solar_token_len_mini(plain_text)
                        # 이전 청크와 합친 결과가 token_limit보다 작으면 병합
                        if combined_length < token_limit:
                            previous_llm_chunk = llm_chunk.pop() # LLM 청크에서 이전 청크 제거
                            previous_retrieve_chunk = retrieve_chunk.pop() # Retrieve 청크에서 이전 청크 제거
                            # 현재 청크와 이전 청크를 병합
                            chunk = previous_llm_chunk + chunk
                            plain_text = previous_retrieve_chunk + plain_text

                    # LLM 청크와 Retrieve 청크 리스트에 각각 추가
                    llm_chunk.append(chunk)
                    retrieve_chunk.append(plain_text)
                    
                except Exception as e:
                    log.warning("Error processing individual chunk: %s", e)

            # 0번 인덱스의 길이가 overlap_tokens 이하인 경우 처리
            if len(retrieve_chunk) > 1 and solar_token_len_mini(retrieve_chunk[0]) < overlap_tokens:
                if solar_token_len_mini(retrieve_chunk[0] + retrieve_chunk[1]) < token_limit:
                    # 첫 번째 청크를 제거하고 다음 청크와 병합
                    retrieve_chunk_idx0 = retrieve_chunk.pop(0)
                    llm_chunk_idx0 = llm_chunk.pop(0)
                    
                    # 병합된 청크를 다시 리스트의 첫 번째 위치에 삽입
                    retrieve_chunk[0] = retrieve_chunk_idx0 + retrieve_chunk[0]
                    llm_chunk[0] = llm_chunk_idx0 + llm_chunk[0]

            # 최종적으로 retrieve_chunk이 token_limit를 넘지 않도록 검증 및 조정
            adjusted_retrieve_chunk = []
            for chunk in retrieve_chunk:
                # cumulative_text: 지금까지 조정된 청크와 현재 청크를 합침
                #combined_text = " ".join(adjusted_retrieve_chunk + [chunk])
                token_count = solar_token_len_mini(chunk)
                if token_count > token_limit:
                    log.info("Trimming retrieve_chunk as token lenght exceeds max tokens ({} tokens)".format(token_count))
                    trimmed_chunk = self.truncate_to_4000_tokens(chunk, tokenizer_mini, max_tokens=token_limit) # token_limit까지 잘라내기 위해 truncate 함수 사용
                    adjusted_retrieve_chunk.append(trimmed_chunk)
                else:
                    adjusted_retrieve_chunk.append(chunk)

            # 기존 retrieve_chunk와 llm_chunk는 각각 단위 청크 리스트로 생성되었음
            # final_llm_chunks, final_retrieve_chunks = accumulate_chunks(llm_chunk, retrieve_chunk, solar_token_len_mini, token_limit)
        
            # 각 청크별로 결과 딕셔너리 구성 (키: 청크 번호)
            chunk_results = {}
            for idx in range(len(llm_chunk)):
                # 줄바꿈, 구분자 제거 처리
                llm_text = llm_chunk[idx].replace('\n\n', ' ').replace("�", "")
                retrieve_text = retrieve_chunk[idx].replace('\n\n', ' ').replace("�", "")
                chunk_results[str(idx + 1)] = {
                    "llm_content": llm_text,
                    "retrieve_content": retrieve_text,
                    "llm_token_count": solar_token_len_pro(llm_text),
                    "retrieve_token_count": solar_token_len_mini(retrieve_text)
                }

            log.info("Chunk split processed successfully.")
            return chunk_results
        except Exception as e:
            log.error("Error during chunk split processing: %s", e)
            return {}, {}
        
    def truncate_to_4000_tokens(self, content, tokenizer_function, max_tokens=3900):
        """
        주어진 텍스트를 최대 max_tokens만큼 토큰으로 자르는 함수 - 최종 검증용
        
        Args:
            content (str): 입력 텍스트
            tokenizer_function (function): 텍스트에서 토큰 ID를 반환하는 함수
            max_tokens (int): 허용되는 최대 토큰 수 (default: 3900).
        
        Returns:
            content or truncated_content (str): 기준 미만이면 원래 텍스트 반환, 기준 이상이면 토큰 제한 내에 들어맞도록 잘린 텍스트 반환
        """
        tokens = tokenizer_function.encode(content)
        
        if len(tokens.ids) >= max_tokens:
            truncated_tokens = tokens.ids[:max_tokens]  # 4000 토큰까지만 가져오기
            truncated_content = tokenizer_function.decode(truncated_tokens)  # 토큰을 다시 텍스트로 디코딩
            return truncated_content
        
        return content  # 토큰 수가 4000 이하인 경우 원래 텍스트 반환