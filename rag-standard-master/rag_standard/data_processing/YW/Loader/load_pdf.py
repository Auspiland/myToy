import os, re, pdfplumber, markdown, fitz, sys
import pymupdf4llm as p4m
from datetime import datetime, timedelta
from markdown.extensions.tables import TableExtension

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger

global log
log = setup_logger.setup_logger('LoadPDF', 'load_pdf')

class LoadPDF:
    """
    load_pdf만 호출하면 됨
    - clean_repeated_text로 첫 페이지가 이상하게 추출되는 경우 처리 (pdfplumber로 로드할 경우에만 해당되는 처리) <- 그림자가 있는 제목의 경우 나타나는 문제
    - extract_table로 테이블 추출
    - get_pdf_mod_date로 수정일자와 생성일자 추출 <- parse_pdf_date로 날짜 파싱
    """
    def __init__(self):
        pass

    def load_pdf(self, file_path):
        """
        PDF 파일을 로드하고 내용을 추출하는 함수 >> PDFPlumber(텍스트), PyMuPDF4LLM(테이블) 사용
        
        Args:
            file_path (str): PDF 파일 경로
            
        Returns:
            tuple: (파일명, 확장자, 수정일자, 생성일자, 텍스트만 추출한 딕셔너리, 텍스트와 테이블을 모두 추출한 딕셔너리, 전체 텍스트를 저장한 문자열)
            - 파일 로드 실패 시 True 반환 (오류 표시용)

        딕셔너리 형식:
            {
                '페이지 번호': 페이지 내용,
                '페이지 번호': 페이지 내용,
                ...
            }
        """
        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1) # 파일명과 확장자 분리

        try:
            # PDF 파일의 수정일자와 생성일자 가져오기
            modified_date, created_date = self.get_pdf_mod_date(file_path)

            text_only_result = []
            with pdfplumber.open(file_path) as pdf:
                # 모든 페이지 순회 (1부터 시작하는 페이지 번호 부여)
                for page_number, page in enumerate(pdf.pages, start=1):
                    text = re.sub(r"·{2,}", "···", page.extract_text())

                    if text and re.search(r'\(cid:\d+\)', text):
                        # (cid:숫자) 형태가 발견되면 fitz로 재시도
                        text = self.extract_text_with_fitz(file_path, page_number - 1)
                    
                    if text:
                        # 첫 페이지에만 중복 문자 정리 적용 (표지 페이지에 장식용 반복 문자가 있을 수 있음)
                        if page_number == 1:
                            text = self.clean_repeated_text(text)
                        # 추출된 텍스트를 리스트에 추가
                        text_only_result.append(text)
                    else:
                        # 텍스트가 없는 페이지는 빈 문자열 추가 (인덱스 동기화 유지)
                        text_only_result.append("")

            # PDF에서 테이블 추출
            tables = self.extract_table(file_path)
            
            text_and_table_result = []

            # 각 페이지별로 텍스트와 테이블 데이터 결합
            for i, (txt, table_data) in enumerate(zip(text_only_result, tables.values()), start=1):
                text_and_table_result.append(txt + '\n' + table_data)

            # 모든 페이지의 텍스트 내용을 하나의 문자열로 합치기 (각 페이지 사이에 두 줄 개행)
            total_text_table = "\n\n".join(text_and_table_result)

            log.info(f"Completed loading pdf file: {os.path.basename(file_path)}")
    
        except Exception as e:
            log.error(f"Cannot load PDF file: {file_path} due to {e}")
            return True

        # 결과 반환: (파일명, 확장자, 수정일, 생성일, 텍스트만 있는 페이지별 딕셔너리, 텍스트와 테이블이 함께 있는 페이지별 딕셔너리)
        return (file_name_without_ext, extension.lower(), modified_date, created_date, {str(i+1):text_only_result[i] for i in range(len(text_only_result))}, {str(i+1):text_and_table_result[i] for i in range(len(text_and_table_result))}, total_text_table)

    def clean_repeated_text(self, text):
        """ 첫 페이지의 중복 문자 정리 적용하는 함수 (표지 페이지에 장식용 반복 문자가 있을 수 있음) """
        # 1. 모든 문자(특수문자 포함)가 3번 이상 반복될 경우 1~2개만 남김 (예: 'AAA' -> 'A', 'a---' -> 'a-')
        cleaned_text = re.sub(r'([\S-])\1{2,}', r'\1', text)  
    
        # 2. 공백이 여러 개 반복되면 하나로 줄임 (예: '텍스트    샘플' -> '텍스트 샘플')
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
        return cleaned_text

    def extract_text_with_fitz(self, file_path, page_index):
        """ fitz(PyMuPDF)로 텍스트 재추출 """
        try:
            with fitz.open(file_path) as pdf:
                page = pdf.load_page(page_index)
                text = page.get_text("text")
                return text.strip()
        except Exception as e:
            err_log.error(f"fitz extraction error at page {page_index+1}: {e}")
            return ""

    def extract_table(self, path:str)->str:
        '''
        PDF 파일에 표와 텍스트가 섞여 있을 때, 각각을 따로 인식해서 추출하는 함수
        텍스트에서 표를 나타내는 마크다운 기호 인식
        '''
        mdn = p4m.to_markdown(path)
        markdown_text = re.sub(r'#{2,}', '', mdn).split('-'*5)
        filtered = {}
        for i in range(len(markdown_text)):
            table_pattern = r'\|.*?\|\s*\n(?:\|.*?\|\s*\n)+' #텍스트에서 표 추출 (정규식)
            tables = re.findall(table_pattern, markdown_text[i], re.MULTILINE)
            html_tables = [markdown.markdown(tbl, extensions=[TableExtension()]) for tbl in tables]
            filtered[i+1] = '\n'.join(html_tables)
        return filtered

    def get_pdf_mod_date(self, file_path):
        """
        PDF 파일의 수정일자와 생성일자를 반환하는 함수
        메타데이터에서 날짜를 추출하며, 실패시 파일 시스템의 날짜 정보를 사용
        
        Args:
            file_path: PDF 파일 경로
            
        Returns:
            tuple: (수정일자, 생성일자) 타임스탬프
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                # PDF 메타데이터에서 날짜 정보 추출
                mod_date = pdf.metadata.get('ModDate', None)
                crt_date = pdf.metadata.get('CreationDate', None)
                
                # 메타데이터 날짜가 없는 경우 파일 시스템 날짜 사용
                if not mod_date:
                    mod_date = os.path.getmtime(file_path)
                else:
                    mod_date = self.parse_pdf_date(mod_date) or os.path.getmtime(file_path)
                    
                if not crt_date:
                    crt_date = os.path.getctime(file_path)
                else:
                    crt_date = self.parse_pdf_date(crt_date) or os.path.getctime(file_path)
                    
                return mod_date, crt_date
                
        except Exception as e:
            log.error(f"Error: {e}")
            return os.path.getmtime(file_path).strftime("%Y-%m-%d %H:%M:%S"), os.path.getctime(file_path).strftime("%Y-%m-%d %H:%M:%S")
        
    def parse_pdf_date(self, pdf_date):
        """
        PDF 메타데이터의 날짜 문자열을 파싱하는 함수
        
        Args:
            pdf_date: PDF 메타데이터의 날짜 문자열 (형식: D:YYYYMMDDHHMMSS+hh'mm')
            
        Returns:
            float: 유닉스 타임스탬프 형식의 날짜, 파싱 실패시 None
        """
        # PDF 날짜 형식 파싱 (D:YYYYMMDDHHMMSS+hh'mm')
        match = re.match(r"D:(\d{14})([+-]\d{2})'(\d{2})'", pdf_date)
        if match:
            date_str, tz_hour, tz_minute = match.groups()
            # 기본 날짜 파싱
            date_obj = datetime.strptime(date_str, "%Y%m%d%H%M%S")
            # 타임존 보정
            offset = timedelta(hours=int(tz_hour), minutes=int(tz_minute))
            date_obj = date_obj + offset
            return date_obj.strftime("%Y-%m-%d %H:%M:%S") # .timestamp()
        return None