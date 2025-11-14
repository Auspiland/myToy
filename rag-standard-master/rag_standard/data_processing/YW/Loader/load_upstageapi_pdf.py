import os, pdfplumber, fitz, requests, json, re, sys
from . import load_pdf
from bs4 import BeautifulSoup
from tokenizers import Tokenizer

loadpdf = load_pdf.LoadPDF()
# tokenizer
tokenizer_pro = Tokenizer.from_pretrained("upstage/solar-pro-tokenizer")
tokenizer_mini = Tokenizer.from_pretrained("upstage/solar-1-mini-tokenizer")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger, config_setting

global log
log = setup_logger.setup_logger('LoadUPSTAGE', 'load_upstage')
config_path = os.path.join(BASE_DIR, 'configs', 'main_config.yaml')
config = config_setting.load_yaml_config(config_path)

def count_pdf_page(pdf_path):
    """ pdf 파일의 페이지 수 반환 """
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)

def remove_html_tags(text):
    """ HTML 태그를 제거하고 순수 텍스트만 추출하는 함수 """
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=' ')

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
            """
            토큰 수 반환 함수
            solar-pro-tokenizer : solar-pro
            """
            tokens = tokenizer_pro.encode(text)
            return len(tokens.ids)
    
        def solar_token_len_mini(text):
            """
            토큰 수 반환 함수
            solar-1-mini-tokenizer : embedding-query, embedding-passage
            """
            tokens = tokenizer_mini.encode(text)
            return len(tokens.ids)

        return solar_token_len_pro, solar_token_len_mini

    except Exception as e:
        log.error("Tokenizer Initialization Error: %s", e)
        return None, None

class UPSTAGE:
    """
    preprocess_api만 호출하면 됨
    - split_pdf_disk로 100페이지가 넘는 문서에 대해서 물리적으로 분리해서 저장
    - upstage_api로 Upstage API 호출
    - merge_jsons_in_directory로 분리했던 문서의 처리된 JSON 파일들 병합 <- merge_json_files로 JSON 파일들 병합
    - merge_with_page로 페이지별로 텍스트와 테이블 내용 병합 <- merge_table_caption으로 테이블과 캡션 내용들 병합
    - create_metadata_info로 JSON 데이터로부터 메타데이터 정보 생성
    """
    def __init__(self):
        pass

    def preprocess_api(self, pname, file_path, mid_path, root_path, api_key):
        """
        Upstage API call로 문서 로드 (주로 PDF 파일)

        Arg:
            pname (str): 프로젝트명
            file_path (str): 처리하고자 하는 파일 경로
            mid_path (str): 중간결과물들을 저장하는 폴더 경로
            root_path (str): 모든 원본 파일이나 중간결과물, 최종결과물 등이 저장되는 최상단 폴더 경로
            api_key (str): API 인증 키

        Return:
            tuple: (파일명, 확장자, 수정날짜, 생성날짜, 텍스트만 추출한 딕셔너리, 텍스트와 테이블을 모두 추출한 딕셔너리, 전체 텍스트를 저장한 문자열)

        딕셔너리 형식:
            {
                '페이지 번호': 페이지 내용,
                '페이지 번호': 페이지 내용,
                ...
            }
        """
        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1)  # 파일 이름 # 확장자
        fpath = []
        if count_pdf_page(file_path) > 100:
            os.makedirs(f"{mid_path}/upstage_splitted", exist_ok=True)
            fpath_list = self.split_pdf_disk(file_path, output_dir=f"{mid_path}/upstage_splitted")
            for file in fpath_list:
                fpath.append(file)
        else:
            fpath.append(file_path)
    
        for f in fpath:        
            results = self.upstage_api(f, api_key, output_formats=None, base64_encoding=None, ocr_mode='force', coordinates='true')
            file_name_wo_ext, ext = os.path.basename(f).rsplit('.', 1)

            os.makedirs(f"{mid_path}/upstage_json", exist_ok=True)
            with open(f"{mid_path}/upstage_json/{file_name_wo_ext}.json", "w", encoding="utf-8-sig") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
        os.makedirs(f"{mid_path}/upstage_merged", exist_ok=True)
        merged_file_path = self.merge_jsons_in_directory(f"{mid_path}/upstage_json", f"{mid_path}/upstage_merged")
        
        for merged in merged_file_path:
            with open(merged, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            page_content = self.merge_with_page(data['elements'], data['usage']['pages'])
            metadata_info = self.create_metadata_info(file_path, data, page_content)
            
            result = {
                "api": data.get("api"),
                "content": data.get("content", {}),
                "elements": data.get("elements", []),
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "metadata": metadata_info  # Add metadata at root level
            }

            os.makedirs(f"{root_path}/{pname}/Loader/UpstageAPI", exist_ok=True)
            with open(f'{root_path}/{pname}/Loader/UpstageAPI/{file_name_without_ext}.json', "w", encoding="utf-8-sig") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                
            log.info(f"Loaded metadata saved at {root_path}/{pname}/Loader/UpstageAPI/{file_name_without_ext}.json")
            
        if extension.lower() == 'pdf':
            modified, created = loadpdf.get_pdf_mod_date(file_path)
        else:
            modified, created = None, None

        log.info(f"Completed loading upstageapi result: {os.path.basename(file_path)}")
            
        return (file_name_without_ext, extension.lower(), modified, created, {page: data["content"]["retrieve_content"] for page, data in page_content.items()}, {page: data["content"]["llm_content"] for page, data in page_content.items()}, result['metadata']['content']['llm_content'])

    def split_pdf_disk(self, pdf_path, output_dir, max_pages=100):
        """
        pdf 파일을 max_pages 크기로 분할하여 디스크에 물리적으로 저장
    
        parameter:
            pdf_path (str): pdf 파일의 경로
            output_dir (str): 분할된 pdf 파일을 저장할 디렉토리 경로
            max_pages (int): 분할할 페이지 수 크기 (default: 100)
    
        return:
            list[str]: 분할된 pdf 데이터 리스트
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        split_files = []
        
        input_pdf = fitz.open(pdf_path)
        total_pages = input_pdf.page_count
        start_page = 0
        part_num = 1
    
        # 페이지를 max_pages씩 분할
        while start_page < total_pages:
            end_page = min(start_page + max_pages, total_pages) - 1
            output_file_path = os.path.join(output_dir, f"{base_name}_{part_num}.pdf")
    
            # 새로운 PDF 파일 생성
            with fitz.open() as output_pdf:
                output_pdf.insert_pdf(input_pdf, from_page=start_page, to_page=end_page)
                output_pdf.save(output_file_path)
    
            split_files.append(output_file_path)
            start_page += max_pages
            part_num += 1
    
        input_pdf.close()
    
        return split_files

    def upstage_api(self, filename, api_key, output_formats=None, base64_encoding=None, ocr_mode='force', coordinates='true'):
        """
        Upstage API 호출
    
        parameter:
            filename (str): 처리하고 있는 파일 경로
            api_key (str): API 인증 키
            output_format (list or None): 출력 형식 (default: ['html', 'text', 'markdown'])
            base64_encoding (list or None): 인코딩 형식 (default: ['table', 'figure', 'chart', 'equation'])
            ocr_mode (str): OCR 모드 (default: 'force')
            coordinates (str): 좌표 포함 여부 (default: 'true')
    
        return:
            response: API 응답 객체
        """
        url = config['upstage_api_settings']['url']
        headers = {"Authorization": f"Bearer {api_key}"}
    
        files = {"document": open(filename, "rb")}
        data = {
            "output_formats": str(output_formats) if output_formats else "['html', 'text', 'markdown']",
            "base64_encoding": str(base64_encoding) if base64_encoding else "['table', 'figure', 'chart', 'equation']",
            "ocr": ocr_mode or "force",
            "coordinates": coordinates or "true",
            "model": config['upstage_api_settings']['model']
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json()

    def merge_jsons_in_directory(self, directory_path, output_path):
        """
        지정한 디렉토리 내의 JSON 파일들을 파일명 접두어(예: "파일명")를 기준으로 그룹화하여 병합한 후,
        하나의 JSON 파일(각 그룹별 병합 결과를 포함하는 구조)로 저장하는 함수
    
        Args:
            directory_path (str): JSON 파일들이 위치한 디렉토리 경로
            output_path (str): 병합된 JSON 파일을 저장할 디렉토리 경로
    
        Returns:
            output_file (str): 병합된 JSON 파일의 저장 경로 (실패 시 False)
        """
        try:
            log.info("Merging JSON files in directory: %s", directory_path)
            
            # 디렉토리 내의 모든 .json 파일 목록 가져오기
            json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
            if not json_files:
                log.warning("No JSON files found in directory: %s", directory_path)
                return False
    
            # 파일명(확장자 제외)에서 공통 접두어를 추출하기 위한 정규식
            pattern = re.compile(r"(.+)_\d+$")
    
            # 그룹화: 공통 접두어를 키로, 해당 그룹의 파일 전체 경로를 값으로 저장
            groups = {}
            for file in json_files:
                basename = os.path.splitext(file)[0]  # 확장자 제거
                match = pattern.match(basename)
                if match:
                    group_name = match.group(1)
                else:
                    # 정규식에 맞지 않으면 파일명 전체를 그룹명으로 사용
                    group_name = basename
                file_path = os.path.join(directory_path, file)
                groups.setdefault(group_name, []).append(file_path)
            
            # 각 그룹별로 merge_json_files 함수를 호출하여 병합 수행
            merged_result = {}
            for group_name, file_paths in groups.items():
                if len(file_paths) > 1: # 병합할 페이지가 있는 경우에만 수행
                    # 파일명을 기준으로 숫자 순 정렬: "파일명_숫자.json"에서 숫자를 추출하여 정렬
                    sorted_file_paths = sorted(
                        file_paths,
                        key=lambda x: int(re.search(r"_(\d+)\.json$", os.path.basename(x)).group(1)) 
                        if re.search(r"_(\d+)\.json$", os.path.basename(x)) else 0
                    )
                    merged_data = merge_json_files(sorted_file_paths)
                    merged_result[group_name] = merged_data
                else:
                    for file_path in file_paths:
                        with open(file_path, 'r', encoding='utf-8-sig') as f:
                            data = json.load(f)
                        merged_result[group_name] = data
                
            merged_fpath = []
    
            # 모든 그룹의 병합 결과를 하나의 JSON 파일로 저장
            for key, value in merged_result.items():
                output_file = os.path.join(output_path, f"{key}.json")
                with open(output_file, "w", encoding="utf-8-sig") as f:
                    json.dump(value, f, ensure_ascii=False, indent=2)
                merged_fpath.append(output_file)
    
            log.info("Merged JSON saved to: %s", output_file)
            return merged_fpath
    
        except Exception as e:
            log.error("Unexpected error occurred while merging JSON files: %s", e)
            return False

    def merge_json_files(self, file_paths):
        """
        정렬되어 들어온 JSON 파일 리스트를 병합
    
        Args:
            file_paths (list): 파일명 끝에 붙은 숫자 순으로 정렬된 파일 리스트 (ex. 파일명_1.json, 파일명_2.json, ...)
    
        Returns:
            merged_data (dict): 병합된 JSON 데이터

        딕셔너리 형식:
            바로 아래의 merged_data 기본 틀 정의한 걸 참고할 것
        """
        # 병합된 데이터를 저장할 기본 구조 초기화
        merged_data = {
            "api": None,
            "content": {"html": "", "markdown": "", "text": ""},
            "elements": [],
            "model": None,
            "usage": {"pages": 0},
        }
    
        # elements 배열의 id를 순차적으로 부여하기 위한 카운터
        last_id = -1  # 이전 파일들의 마지막 id 값 (0부터 시작하도록 -1로 초기화)
        
        # 페이지 번호를 순차적으로 부여하기 위한 카운터
        last_page = 0 # 이전 파일들의 마지막 page 값
    
        # 입력받은 파일 리스트를 순회하며 병합 작업 수행
        for file_path in file_paths:
            try:
                # JSON 파일 읽기
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
        
                # api 필드 검증: 모든 파일의 api 값이 동일해야 함
                if merged_data["api"] is None:
                    merged_data["api"] = data["api"]
                elif merged_data["api"] != data["api"]:
                    raise ValueError(f"Inconsistent 'api' value in file: {file_path}")
        
                # content 필드 병합: 텍스트 내용을 순차적으로 이어붙임 (그대로 병)
                for content_type in ["html", "markdown", "text"]:
                    merged_data["content"][content_type] += data["content"].get(content_type, "")
        
                # elements 배열 병합: id와 페이지 번호를 연속되게 재할당 (id, page 번호를 순차적으로 증가)
                if data["elements"]:
                    # 현재 파일의 최대 페이지 번호 계산
                    max_page_in_current_file = max(
                        element.get("page", 1) for element in data["elements"]
                    )
    
                    # 각 element 처리
                    for element in data["elements"]:
                        new_element = element.copy()
                        
                        # ID  순차 할당 (1씩 증가시켜 할당)
                        last_id += 1
                        new_element["id"] = last_id
                        
                        # 페이지 번호 재할당: 현재 파일 내의 상대적 페이지 번호를 계산
                        relative_page = element.get("page", 1)
                        # 이전 파일들의 최대 페이지 수를 기준으로 새로운 페이지 번호 할당
                        new_element["page"] = last_page + relative_page
                        
                        merged_data["elements"].append(new_element)
                    
                    # 다음 파일을 위해 마지막 페이지 번호 업데이트
                    last_page += max_page_in_current_file
        
                # model 필드 검증: 모든 파일의 model 값이 동일해야 함
                if merged_data["model"] is None:
                    merged_data["model"] = data["model"]
                elif merged_data["model"] != data["model"]:
                    raise ValueError(f"Inconsistent 'model' value in file: {file_path}")
        
                # usage 필드 병합: 페이지 수 합산
                merged_data["usage"]["pages"] += data["usage"]["pages"]
    
            except json.JSONDecodeError as e:
                log.error("Error decoding JSON in file %s: %s", file_path, e)
                return None
            except KeyError as e:
                log.error("Missing expected key in file %s: %s", file_path, e)
                return None
            except Exception as e:
                log.error("Unexpected error processing file %s: %s", file_path, e)
                return None
    
        return merged_data

    def merge_with_page(self, elements, total_page):
        """
        elements에서 텍스트와 테이블 HTML을 페이지별로 병합하고,
        테이블 주변 캡션을 병합하여 테이블에 포함시키는 함수
    
        Args:
            elements (list): JSON 요소들의 리스트. 이 함수에서 사용되는 주요 키:
                - page (int): 페이지 번호
                - category (str): 요소의 카테고리 (text, table, figure, chart 등)
                - content (dict): 
                    - text (str): 텍스트 내용 (일반 텍스트 요소의 경우)
                    - html (str): HTML 내용 (테이블 요소의 경우)
            total_page (int): 전체 페이지 수
    
        Returns:
            page_content (dict): 페이지별로 병합된 텍스트 내용
            - 오류 발생 시 빈 딕셔너리({}) 반환

        딕셔너리 형식:
            {
                "content": {
                    "llm_content": 텍스트와 테이블을 추출한 내용,
                    "retrieve_content": 텍스트로만 추출한 내용
                },
                "llm_token_count": llm_content을 기준으로 센 토큰 수
            }
        """
        solar_token_len_pro, solar_token_len_mini = initialize_tokenizer()
        try:
            log.info("Extracting and merging text from elements...")
            # 페이지별로 요소를 저장할 딕셔너리 (각 요소는 dict로 저장)
            page_elements = {}
        
            for element in elements:
                try:
                    page_num = int(element.get("page", 1))  # 기본값: 1
                    if page_num not in page_elements:
                        page_elements[page_num] = []
        
                    # 특정 카테고리 제외: chart, equation, header, footer
                    if element['category'] in ["chart", "equation", "header", "footer"]:
                        continue
        
                    # 테이블이 아닌 일반 텍스트 요소 처리
                    if element['category'] != 'table':
                        # HTML 내용 정제 (줄바꿈, 특수문자 제거)
                        content = re.sub(r'\n+', ' ', element.get('content', {}).get('html', '')).replace("�", "")
                        if content:
                            page_elements[page_num].append({
                                "category_ele": "text",
                                "content": content,
                                "token_cnt": solar_token_len_mini(content)
                            })
                    # 테이블 요소 처리
                    else:
                        # HTML 내용 정제 (줄바꿈, 특수문자, <br> 태그 제거)
                        content = re.sub(r'\n+', ' ', element.get('content', {}).get('html', '')).replace("�", "").replace("<br>", "")
                        if content:
                            page_elements[page_num].append({
                                "category_ele": "table",
                                "content": content,
                                "token_cnt": solar_token_len_mini(content)
                            })
        
                except KeyError as e:
                    log.error("Missing expected key in element: %s (%s)", element, e)
                except Exception as e:
                    log.error("Unexpected error processing element: %s (%s)", element, e)
                    continue
        
            modified_page_elements = self.merge_table_caption(page_elements, solar_token_len_mini)
        
            # 페이지별로 요소들의 content를 하나의 문자열로 병합
            page_content = {
                str(page): {
                    "content": {
                        "llm_content": "\n".join([e['content'] for e in elems]),
                        "retrieve_content": remove_html_tags("\n".join([e['content'] for e in elems]))
                    },
                    "llm_token_count": solar_token_len_mini("\n".join([e['content'] for e in elems]))
                }
                for page, elems in sorted(modified_page_elements.items())
                if elems  # 비어 있지 않은 페이지만 포함
            }
        
            log.info("Successfully merged text from %d elements.", total_page)
            return page_content
        
        except Exception as e:
            log.error("Unexpected error occurred while extracting text: %s", e)
            return {}

    def merge_table_caption(self, page_elements, solar_token_len_mini):
        """
        페이지 내에서 테이블과 캡션을 병합할 때 사용하는 함수

        Args:
            page_elements (dict): 페이지별로 카테고리와 내용, 토큰 수를 저장한 딕셔너리
            solar_token_len_mini (function): solar-mini 토크나이저로 토큰 수를 계산하는 함수

        Return:
            page_element (dict): 페이지별로 테이블과 캡션을 처리한 딕셔너리

        딕셔너리 형식:
            {
                '페이지 번호': {
                    'category_ele': 카테고리,
                    'content': 페이지 내용,
                    'token_cnt': 페이지 토큰 수
                }
            }
        """
        window_size = 5
        max_caption_length = 150
        for page, elems in page_elements.items():
            # 리스트 내 테이블 요소의 인덱스 찾기
            table_indices = [i for i, e in enumerate(elems) if e['category_ele'] == 'table']
            # 캡션으로 사용된 요소들의 인덱스를 제거하기 위한 집합
            remove_indices = set()
    
            for table_idx in table_indices:
                target_index = []
                # 앞쪽 캡션 요소 탐색 (가까운 순서부터)
                token_sum = 0
                front_indices = list(range(max(0, table_idx - window_size), table_idx))[::-1]
                for idx in front_indices:
                    if elems[idx]['category_ele'] == 'table':
                        break
                    if token_sum + elems[idx]['token_cnt'] < max_caption_length:
                        target_index.insert(0, idx)
                        token_sum += elems[idx]['token_cnt']
                    else:
                        break
    
                # 뒤쪽 캡션 요소 탐색
                token_sum = 0
                back_indices = list(range(table_idx + 1, min(len(elems), table_idx + window_size + 1)))
                for idx in back_indices:
                    if elems[idx]['category_ele'] == 'table':
                        break
                    if token_sum + elems[idx]['token_cnt'] < max_caption_length:
                        target_index.append(idx)
                        token_sum += elems[idx]['token_cnt']
                    else:
                        break
    
                # 캡션과 테이블 내용을 병합 (구분자 "�" 사용)
                merged_caption_text = "�"
                for idx in target_index:
                    merged_caption_text += " " + elems[idx]['content']
                table_merged_caption_text = merged_caption_text + elems[table_idx]['content']
    
                # 테이블 요소 업데이트
                elems[table_idx]['content'] = table_merged_caption_text
                elems[table_idx]['token_cnt'] = solar_token_len_mini(table_merged_caption_text)
                # 캡션으로 사용된 요소는 최종 병합 결과에서 제거
                remove_indices.update(target_index)
    
            # 캡션 요소 제거 (중복되지 않도록)
            if remove_indices:
                page_elements[page] = [e for i, e in enumerate(elems) if i not in remove_indices]
        
        return page_elements

    def create_metadata_info(self, file_path, data, page_content):
        """
        JSON 데이터로부터 메타데이터 정보 생성
        
        Args:
            file_path (str): 처리하고자 하는 파일 경로
            data (dict): 만약 페이지 때문에 나뉘었다면 다시 병합한 JSON 파일 내용 (나뉘지 않았다면 그냥 그 API 호출했던 JSON 파일 내용)
            page_content (dict): 페이지별로 병합된 텍스트 내용
        
        Returns:
            metadata (dict): 생성된 메타데이터 정보
            - False: 오류 발생 시

        딕셔너리 형식:
            아래의 metadata 정의한 틀 참고할 것
        """
        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1)
        try:
            log.info("Creating metadata info...")
            
            text_content = data.get("content", "").get("text", "") # retrieve text
            # html_content = data.get("content", "").get("html", "") # html
            
            metadata = {
                # 파일 정보
                'info': {
                    'file_path': file_path,
                    'file_name': file_name_without_ext,
                    'extension': extension
                },
                # 컨텐츠 정보
                "content": {
                    "retrieve_content": re.sub(r'\n{2,}', ' ',  text_content).replace("�", ""),
                    "llm_content": "\n\n".join(page_data["content"]["llm_content"] for page_data in page_content.values() if "content" in page_data) #content for content in page_content.values()) # paragraph 구분자 추가 : "\n\n"
                },
                # 페이지별 내용
                "page_content": page_content
            }
            
            log.info("Metadata info created successfully with %d pages.", len(page_content))
            
            return metadata
            
        except Exception as e:
            log.error("Error creating metadata info: %s", e)
            return False