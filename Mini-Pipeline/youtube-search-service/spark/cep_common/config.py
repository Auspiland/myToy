import os
import importlib

_env = os.environ.get("CEP_ENV", "local")

try:
    module = importlib.import_module(f"conf.{_env}.properties")
    for name in dir(module):
        if not name.startswith('_'):
            globals()[name] = getattr(module, name)
except ModuleNotFoundError as e:
    raise ImportError(f"환경 설정 파일을 찾을 수 없습니다: conf/{_env}/properties.py") from e



