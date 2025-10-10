import os, sys
import re, json, logging
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,                    # 출력 레벨: DEBUG/INFO/WARNING/ERROR/CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)



API_KEY   = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=API_KEY)

def response_GPT(system_prompt="", user_prompt=None, messages=None, model="gpt-5"):
    if not user_prompt and not messages:
        raise ValueError("LLM 입력값이 없습니다.")
    resp = client.responses.create(
        model=model,
        input=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ] if not messages else messages,
    )
    text = resp.output_text
    return text

def clean_filename(name: str, platform: str = "win") -> str:
    s = str(name)
    if platform == "win":
        s = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", s)  # 금지 문자
        s = re.sub(r"[\. ]+$", "", s) or "_"          # 끝 공백/점 금지
        if re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?$', s or "_"):
            s = "_" + s                               # 예약어 회피
    else:  # posix
        s = re.sub(r'[/\x00]', "_", s or "_")         # '/'와 NUL 금지
    return (s or "_")[:255]                           # 길이 제한


def extract_json(text):
    # 1) 그대로 시도
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 2) ```json ... ``` 블록 추출
    s = text.find("```json")
    if s != -1:
        s = text.find("\n", s)
        e = text.find("```", s + 1)
        if s != -1 and e != -1:
            blk = text[s+1:e].strip()
            try:
                return json.loads(blk)
            except json.JSONDecodeError:
                pass
    # 3) 첫 { .. } 범위 추정
    l = text.find("{")
    r = text.rfind("}")
    if l != -1 and r != -1 and r > l:
        try:
            return json.loads(text[l:r+1])
        except json.JSONDecodeError:
            pass
    raise ValueError("JSON 파싱 실패")
