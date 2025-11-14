import os, re, sys
import olefile, zlib, struct
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) # 상대경로로 root 설정 (Rag_Standard_v2)
sys.path.append(BASE_DIR)
from rag_standard.utils import setup_logger

global log
log = setup_logger.setup_logger('LoadHWP', 'load_hwp')

class LoadHWP:
    """ load_hwp만 호출하면 됨 <- hwp_time_to_datetime으로 날짜 처리 """
    def __init__(self):
        pass

    def load_hwp(self, file_path):
        """
        한글 문서(.hwp) 파일을 로드하고 내용을 추출하는 메소드 >> olefile 라이브러리를 활용해서 직접 처리
        
        Args:
            file_path: 한글 문서 파일 경로
            
        Returns:
            tuple: (파일명, 확장자, 수정일, 생성일, 텍스트만 추출한 딕셔너리, 텍스트만 추출한 딕셔너리(원래는 표 추출된 버전이어야 하나, hwp는 표 추출 X), 전체 텍스트를 저장한 문자열)

        >> 참고: HWP는 전체 문서를 하나의 청크로 보고 내용을 추출하기 때문에, 아래와 같은 딕셔너리 형식으로 추출됨
            {
                '1': 문서 내용
            }
        """
        file_name_without_ext, extension = os.path.basename(file_path).rsplit('.', 1) # 파일명과 확장자 분리

        try:
            # OLE 파일 형식으로 한글 파일 열기
            f = olefile.OleFileIO(file_path)
            dirs = f.listdir()

            # HWP 파일 검증 - 필수 디렉토리 확인
            if ["FileHeader"] not in dirs or \
                    ["\x05HwpSummaryInformation"] not in dirs:
                raise Exception("Not Valid HWP.")

            # 메타데이터 추출 (생성 시간, 최종 저장 시간 등)
            meta = {}
            if f.exists("\x05HwpSummaryInformation"):
                meta_stream = f.getproperties("\x05HwpSummaryInformation")
                meta_keys = {
                    12: "create_time", # 문서 생성 시간
                    13: "last_saved_time", # 최종 저장 시간
                }
                for key, label in meta_keys.items():
                    if key in meta_stream:
                        meta[label] = meta_stream[key]
 
            # 문서 포맷 압축 여부 확인 (한글 문서는 압축되어 있을 수 있음))
            header = f.openstream("FileHeader")
            header_data = header.read()
            is_compressed = (header_data[36] & 1) == 1

            # Body Sections 불러오기
            nums = []
            for d in dirs:
                if d[0] == "BodyText":
                    nums.append(int(d[1][len("Section"):]))
            sections = ["BodyText/Section" + str(x) for x in sorted(nums)]

            # 전체 text 추출
            text = ""
            for section in sections:
                # 각 섹션 스트림 열기
                bodytext = f.openstream(section)
                data = bodytext.read()

                # 압축된 경우 압축 해제
                if is_compressed:
                    unpacked_data = zlib.decompress(data, -15)
                else:
                    unpacked_data = data

                # 각 Section 내 text 추출
                section_text = ""
                i = 0
                size = len(unpacked_data)
                while i < size:
                    # 레코드 헤더 파싱
                    header = struct.unpack_from("<I", unpacked_data, i)[0]
                    rec_type = header & 0x3ff # 레코드 타입 (하위 10비트)
                    rec_len = (header >> 20) & 0xfff # 레코드 길이 (상위 12비트)

                    # 텍스트 레코드인 경우 (타입 67)
                    if rec_type in [67]:
                        rec_data = unpacked_data[i + 4:i + 4 + rec_len]
                        section_text += rec_data.decode('utf-16') # UTF-16으로 디코딩
                        section_text += "\n"

                    i += 4 + rec_len

                text += section_text
                text += "\n"
                
            # 텍스트 정제 (비-단어 문자를 공백으로 대체, 불필요한 공백 제거)
            text_only_result = re.sub(' {2,}', ' ', re.sub('\W', ' ', text)).strip()
            text_and_table_result = re.sub(' {2,}', ' ', re.sub('\W', ' ', text)).strip()

            # 메타데이터에서 시간 정보 추출 및 변환
            for key, value in meta.items():
                if key == "create_time":
                    created_date = self.hwp_time_to_datetime(value).strftime('%Y-%m-%d %H:%M:%S')
                if key == "last_saved_time":
                    modified_date = self.hwp_time_to_datetime(value).strftime('%Y-%m-%d %H:%M:%S')

            log.info(f"Completed loading hwp file: {os.path.basename(file_path)}")

        except Exception as e:
            log.info(f"Cannot load HWP file: {file_path} due to {e}")
            return True

        # 결과 반환: (파일명, 확장자, 수정일, 생성일, 텍스트 결과, 표+텍스트 결과) - 텍스트 결과와 표+텍스트 결과는 각각 딕셔너리 형태로 반환 (키: '1')
        return (file_name_without_ext, extension.lower(), modified_date, created_date, {'1':text_only_result}, {'1':text_and_table_result}, text_and_table_result)
    
    def hwp_time_to_datetime(self, date_value):
        """ 한글 문서의 타임스탬프를 datetime 객체로 변환하는 함수 """        
        try:
            # 연도에서 369 빼기
            dt = datetime.fromtimestamp(date_value)
            adjusted_dt = dt.replace(year=dt.year - 369)
            return adjusted_dt
        except ValueError as e:
            log.error(f"Error converting timestamp {timestamp}: {e}")
            return None