import os, re, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger

global log
log = setup_logger.setup_logger('LoadTXT', 'load_txt')

class LoadTXT:
    """
    load_txt만 호출하면 됨
    - normalize_fullwidth_numbers로 전각 숫자를 반각 숫자로 변환
    - remove_spaces_between_digits로 숫자 사이의 공백 제거
    - load_txt로 텍스트 파일을 로드하고 정규화
    """
    def __init__(self):
        pass

    def normalize_fullwidth_numbers(self, text):
        """전각 숫자를 반각 숫자로 변환"""
        return ''.join(
            chr(ord(c) - 0xFEE0) if '０' <= c <= '９' else c
            for c in text
        )

    def remove_spaces_between_digits(self, text):
        """숫자와 숫자 사이의 공백만 제거"""
        return re.sub(r'(?<=\d) (?=\d)', '', text)

    def load_txt(self, file_path, mid_path):
        """
        텍스트 파일을 로드하고 내용을 추출하는 메소드
        
        Args:
            file_path: 텍스트 파일 경로
            mid_path: 변환된 파일을 저장할 출력 폴더 경로
            
        Returns:
            tuple: (파일명, 확장자, 수정일, 생성일, 텍스트만 추출한 딕셔너리, 텍스트와 테이블을 모두 추출한 딕셔너리, 전체 텍스트를 저장한 문자열)
            - 실패 시 False 반환

        딕셔너리 형식:
            {
                'content': 텍스트 내용,
            }
        """
        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1) # 파일명과 확장자 분리

        try:
            # 텍스트 파일 로딩
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = f.read()

            # 텍스트 정규화
            normalized = self.normalize_fullwidth_numbers(raw)
            cleaned = self.remove_spaces_between_digits(normalized)

            # 파일 메타데이터 추출 - txt 파일은 기본적으로 날짜 관련 메타데이터 저장 안 함
            modified_date = os.path.getmtime(file_path)
            created_date = os.path.getctime(file_path)

            # 정규화된 텍스트를 중간 파일로 저장
            os.makedirs(mid_path, exist_ok=True)
            normalized_file_path = os.path.join(mid_path, f"{file_name_without_ext}_normalized.txt")
            with open(normalized_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            log.info(f"Normalizing Complete: {file_path}")

            log.info(f"Completed loading txt file: {os.path.basename(file_path)}")
            
            return (file_name_without_ext, extension.lower(), modified_date, created_date, 
                   {"1": cleaned}, {"1": cleaned}, cleaned)

        except Exception as e:
            log.error(f"[ERROR] Progress Failed: {file_path} - {e}")
            return False