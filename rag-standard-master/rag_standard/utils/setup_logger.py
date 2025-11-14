# rag_standard/utils/log_setup.py
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(logger_name, log_file_name, level=logging.INFO, log_dir_relative="logs"):
    """ 로깅 설정을 초기화하고 logger 인스턴스 반환 """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    log_dir_abs = os.path.join(project_root, log_dir_relative)

    # 로그 파일을 저장할 폴더 지정 및 폴더가 없으면 생성
    if not os.path.exists(log_dir_abs):
        os.makedirs(log_dir_abs)

    # 파일에 로그 기록하기 위한 핸들러 설정
    logger = logging.getLogger(logger_name)
    if not logger.handlers: # Avoid adding multiple handlers if already configured
        logger.setLevel(level)

        log_file_path = os.path.join(log_dir_abs, f'{log_file_name}.log')
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5242880,  # 각 로그 파일의 최대 크기 : 5MB
            backupCount=10     # 최대로 보관할 로그 파일 수 : 10개 (.log, .log.1, .log.2, ...)
        )

        # 로그 메세지 형식 설정 (시간 - 로거 이름 - 로그 레벨 - 메세지 순으로 기록)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 콘솔(터미널)에 로그를 출력하기 위한 핸들러 설정 - 터미널에 로그 출력하고 싶지 않으면 주석 처리하거나 삭제해도 무방
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 로그 메세지가 상위 logger로 전파되는 것을 방지 - 이중 로깅을 막기 위해 필요
        logger.propagate = False
    return logger
