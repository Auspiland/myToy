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

def response_GPT(system_prompt="", user_prompt=None, messages=None, model="gpt-5-nano"):
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

def response_GPT_stream(messages, model="gpt-5-nano"):
    with client.responses.stream(
        model=model,
        input=messages
        # max_output_tokens=800,
    ) as stream:
        parts = []
        for event in stream:
            if event.type == "response.output_text.delta":
                parts.append(event.delta)
        stream.close()
    return "".join(parts)


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


# ====================================================

from openai import APIError, InternalServerError, RateLimitError
import time, random

RETRYABLE_EXC = (InternalServerError, APIError, ConnectionError, TimeoutError)

def _normalize_messages(system_prompt="", user_prompt=None, messages=None):
    if messages:
        return messages
    if not user_prompt and not system_prompt:
        raise ValueError("LLM 입력값이 없습니다.")
    return [
        {"role": "system", "content": system_prompt or ""},
        {"role": "user", "content": user_prompt or ""},
    ]

def response_GPT_with_stream_fallback(
    system_prompt="",
    user_prompt=None,
    messages=None,
    model="gpt-5-nano",
    max_output_tokens=None,
    max_retries=3,
    fallback_stream=True,
):
    """
    1) 기본적으로 비-스트리밍 요청 시도.
    2) 5xx 또는 네트워크 오류 발생 시 지수 백오프 후 재시도.
    3) 반복 실패 시 스트리밍 모드로 폴백.
    """
    msgs = _normalize_messages(system_prompt, user_prompt, messages)

    backoff = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.responses.create(
                model=model,
                messages=msgs,
                **({"max_output_tokens": max_output_tokens} if max_output_tokens else {}),
            )
            return resp.output_text
        except RateLimitError:
            sleep_s = backoff + random.uniform(0, 0.4)
            log.warning(f"[attempt {attempt}] RateLimit, sleep {sleep_s:.2f}s")
            time.sleep(sleep_s)
            backoff = min(backoff * 2, 8.0)
        except RETRYABLE_EXC as e:
            sleep_s = backoff + random.uniform(0, 0.5)
            log.warning(f"[attempt {attempt}] Retryable: {type(e).__name__}, sleep {sleep_s:.2f}s")
            time.sleep(sleep_s)
            backoff = min(backoff * 2, 8.0)
        except Exception as e:
            log.error(f"[attempt {attempt}] Non-retryable: {e}")
            raise

    if not fallback_stream:
        raise RuntimeError("비-스트리밍 실패, 스트리밍 폴백 비활성화.")

    # 스트리밍 폴백
    for attempt in range(1, 3):
        try:
            parts = []
            with client.responses.stream(
                model="gpt-4o",
                messages=msgs,
                **({"max_output_tokens": max_output_tokens} if max_output_tokens else {}),
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta":
                        parts.append(event.delta)
                stream.close()
            return "".join(parts)
        except Exception as e:
            sleep_s = backoff + random.uniform(0, 0.5)
            log.warning(f"[stream attempt {attempt}] Error {type(e).__name__}, sleep {sleep_s:.2f}s")
            time.sleep(sleep_s)
            backoff = min(backoff * 2, 8.0)

    raise RuntimeError("스트리밍 폴백까지 실패했습니다.")
