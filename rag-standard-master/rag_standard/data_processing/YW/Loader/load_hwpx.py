import zipfile, os, re, sys
from bs4 import BeautifulSoup
from texttable import Texttable
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger

global log
log = setup_logger.setup_logger('LoadHWPX', 'load_hwpx')

# 특정 단어를 교체하거나 붙이기 위한 매핑 딕셔너리
replacement_dict = {
    "프 로 그 램": "프로그램",
    "직  급": "직급",
    "소  속": "소속",
    "과  제  명": "과제명",
    "성  명": "성명",
    "구  분": "구분",
    "구 분": "구분",
    "세 부 과 제 명": "세부과제명",
    "전 략 과 제": "전략과제",
    "논 문": "논문",
    "임 금": "임금",
    "연  구 용역비 ": "연구 용역비",
    "목  적": "목적",
    "일 용": "일용",
    "일  반": "일반",
    "연  구": "연구",
}

def apply_replacements(text, replacements):
    """ 특정 단어를 매핑 딕셔너리를 통해 수정 """
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def pad_table_rows(rows):
    """ 표의 행 길이를 가장 긴 행에 맞게 패딩 """
    max_columns = max(len(row) for row in rows)
    for row in rows:
        while len(row) < max_columns:
            row.append("")  # 빈 셀 추가
    return rows

def validate_date_value(val, date_type, file_path):
    """
    날짜 혹은 숫자 형식 여부를 확인하는 함수
    
    Arg:
        val: 메타데이터로부터 추출한 값
        date_type: 'created' 또는 'modified' (어느 타입의 날짜인지)
        file_path: 파일 경로 (파일 시스템 메타데이터를 가져오기 위해 사용)
    
    Return:
        숫자가 포함되어 있으면 val을 그대로 반환
        그렇지 않으면 파일 시스템의 생성 또는 수정 타임스탬프 사용
    """
    if val and re.search(r'\d', val):
        return val
    else:
        log.info("Date Value is not in date or integer format - using the file system metadata")
        if date_type == 'created':
            cm_time = os.path.getctime(file_path)
        elif date_type == 'modified':
            cm_time = os.path.getmtime(file_path)
        else:
            cm_time = None

        return datetime.fromtimestamp(cm_time).strftime('%Y-%m-%d %H:%M:%S') if cm_time is not None else None

class LoadHWPX:
    """ load_hwpx만 호출하면 됨 <- extract_hwpx_metadata로 수정날짜와 생성날짜 정보 추출 """
    def __init__(self):
        pass

    def load_hwpx(self, file_path, mid_path):
        """
        HWPX 파일에서 텍스트와 표를 순서대로 추출하는 함수 >> 메타데이터 정보 읽어서 내용 구성
        
        Args:
            file_path: 한글 문서 파일 경로
            mid_path: 중간 결과물 저장하는 폴더 경로 (여기서는 hwpx metadata 저장하는 곳)
            
        Returns:
            tuple: (파일명, 확장자, 수정일, 생성일, 텍스트만 추출한 딕셔너리, 텍스트와 테이블을 모두 추출한 딕셔너리, 전체 텍스트를 저장한 문자열)

        >> 참고: HWPX는 전체 문서를 하나의 청크로 보고 내용을 추출하기 때문에, 아래와 같은 딕셔너리 형식으로 추출됨
            {
                '1': 문서 내용
            }
        """
        log.info("HWPX 파일 감지: XML 파싱을 시도합니다.")

        text_only = []
        text_table = []

        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1) # 파일명과 확장자 분리
        created, modified = self.extract_hwpx_metadata(file_path)
        
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(f'{mid_path}/extracted_hwpx')
    
        content_path = os.path.join(f'{mid_path}/extracted_hwpx', 'Contents', 'section0.xml')
        if os.path.exists(content_path):
            with open(content_path, 'r', encoding='utf-8') as file:
                # XML 파서로 파싱 (네임스페이스 인식)
                soup = BeautifulSoup(file, 'xml')
    
                # <hp:p>와 <hp:tbl> 태그를 올바르게 가져오기
                elements = soup.find_all(['hp:p', 'hp:tbl'], recursive=True)
    
                if not elements:
                    log.warning("문서에서 텍스트나 표를 찾을 수 없습니다.")
                    return
    
                log.info("문서 내용 처리 시작")
                seen_texts = set()  # 중복 제거를 위한 집합
                table_texts = set()  # 표 내용 저장을 위한 집합
    
                for element in elements:
                    if element.name == 'tbl':
                        # 표 형식화 출력 (표 중복제거용)
                        for row in element.find_all('hp:tr', recursive=True):
                            for cell in row.find_all('hp:tc', recursive=True):
                                # 셀 내부의 <hp:run> 안의 <hp:t> 텍스트 추출
                                for cell_run in cell.find_all('hp:run', recursive=True):
                                    hp_t = cell_run.find('hp:t')
                                    if hp_t:
                                        text = apply_replacements(hp_t.get_text(strip=True), replacement_dict)
                                        table_texts.add(text)  # 표 텍스트 저장
                   
                        # 표 형식화 출력
                        table = Texttable(max_width=100)
                        table_rows = []
                        for row in element.find_all('hp:tr', recursive=True):
                            table_row = []
                            for cell in row.find_all('hp:tc', recursive=True):
                                cell_texts = []
    
                                # 셀 내부의 <hp:run> 안의 <hp:t> 텍스트 추출
                                for cell_run in cell.find_all('hp:run', recursive=True):
                                    hp_t = cell_run.find('hp:t')
                                    if hp_t:
                                        text = apply_replacements(hp_t.get_text(strip=True), replacement_dict)
                                        cell_texts.append(text)
    
                                # Combine texts for the cell
                                combined_text = " ".join(cell_texts)
                                table_row.append(combined_text)
    
                            table_rows.append(table_row)
    
                        # 패딩 적용
                        table_rows = pad_table_rows(table_rows)
    
                        # Render the table
                        table.add_rows(table_rows)
                        table_str = table.draw()
                        text_table.append(table_str)
                        log.info("표 처리 완료")
    
                    elif element.name == 'p':
                        # <hp:p> 태그 안의 <hp:run> 태그에서 데이터 추출
                        for run in element.find_all('hp:run', recursive=False):
                            # hp:t 값 추출
                            hp_t = run.find('hp:t')
                            if hp_t:
                                cleaned_text = apply_replacements(hp_t.get_text(strip=True), replacement_dict)
                                if cleaned_text.strip() and cleaned_text not in seen_texts: # and cleaned_text not in table_texts:
                                    seen_texts.add(cleaned_text)
                                    text_only.append(cleaned_text)
                                    text_table.append(cleaned_text)
                        log.info("텍스트 처리 완료")
                                
            log.info(f"Completed loading hwpx file: {os.path.basename(file_path)}")

            return (file_name_without_ext, extension.lower(), modified, created, {'1': re.sub(' {2,}', ' ', '\n'.join(text_only)).strip()}, {'1': re.sub(' {2,}', ' ', '\n'.join(text_table)).strip()}, re.sub(' {2,}', ' ', '\n'.join(text_table)).strip())
            
        else:
            log.error("HWPX에서 section0.xml 파일을 찾을 수 없습니다.")
            
    def extract_hwpx_metadata(self, file_path):
        """ HWPX 파일의 메타데이터 추출 - 수정날짜와 생성날짜 추출 (HWPX 파일의 메타데이터 내에 정보 없으면 파일 시스템의 메타데이터 정보 활용 """    
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                if 'Contents/content.hpf' in zip_ref.namelist():
                    with zip_ref.open('Contents/content.hpf') as f:
                        content = f.read()
                        
                        if content.startswith(b'<?xml'):
                            try:
                                soup = BeautifulSoup(content, 'xml')
                                
                                # 문서 속성이나 메타데이터 관련 태그 검색
                                property_tags = soup.find_all(['property', 'Properties', 'DocumentProperties', 'meta'])
                                created = None
                                modified = None
        
                                if property_tags:
                                    # print("문서 속성 관련 태그 발견:")
                                    for tag in property_tags:
                                        # print(f"  {tag.name}: {tag.attrs}")
                                        if 'name' in tag.attrs:
                                            tag_name = tag.attrs['name'].lower()
                                            if tag_name in ['createddate', 'created'] and created is None:
                                                created = tag.attrs.get('content')
                                            if tag_name in ['modifieddate', 'modified'] and modified is None:
                                                modified = tag.attrs.get('content')
        
                                # 유효성 검사 후 파일 시스템 메타데이터 보완
                                created = validate_date_value(created, 'created', file_path)
                                modified = validate_date_value(modified, 'modified', file_path)
                                
                                # print("\n날짜 관련 태그 발견:")
                                log.info(f"created: {created}\nmodified: {modified}")
                                return created, modified
                            
                            except Exception as xml_error:
                                log.error(f"content.hpf XML 파싱 오류: {xml_error}")
                        else:
                            log.warning("content.hpf 파일이 XML 형식이 아닙니다.")
                else:
                    log.warning("Contents/content.hpf 파일을 찾을 수 없습니다.")
        
        except Exception as e:
            log.error(f"HWPX 내부 메타데이터 추출 중 오류: {e}")