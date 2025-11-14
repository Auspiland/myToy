# rag_standard/utils/config_setting.py
import os
import yaml
from dotenv import load_dotenv

def load_env(env_path=None):
    """.env 파일 로드 함수"""
    if env_path is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        env_path = os.path.join(project_root, '.env')

    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        print(f"로드된 .env 경로: {env_path}")
        return dict(os.environ)
    else:
        print(f"Warning: .env file을 다음 경로에서 찾을 수 없습니다: {env_path}")
        return {}

def load_yaml_config(config_path: str) -> dict:
    """YAML config 파일 로드 함수"""
    if not os.path.isabs(config_path):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        config_path = os.path.join(project_root, config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config 파일을 다음 경로에서 찾을 수 없습니다: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print(f"로드된 YAML config 경로: {config_path}")
    return config