import os, sys
import re, json, logging, requests
from openai import OpenAI
from pathlib import Path
import subprocess
from typing import Optional
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

def response_GPT_stream(messages, model="gpt-5"):
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
    model="gpt-5",
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


# =============================================================
# github 자동 업로드 관련 코드
# =============================================================


def push_to_github(file_path: str) -> str:
    """
    주어진 파일을 현재 Git 리포지토리의 기본 브랜치로 푸시하고,
    GitHub 웹에서 열 수 있는 HTTPS URL을 반환합니다.
    - 리포 루트/브랜치/remote URL을 Git에서 동적으로 조회
    - 변경 사항 없으면 commit 생략
    - origin 미설정/인증 오류/브랜치 오류 등을 명확히 안내
    """
    file_path = Path(file_path).resolve()

    def _run(cmd, cwd=None):
        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    # 1) 리포 루트 자동 탐지 (파일이 속한 디렉터리 기준)
    repo_root_res = _run(["git", "-C", str(file_path.parent), "rev-parse", "--show-toplevel"])
    if repo_root_res.returncode != 0:
        raise RuntimeError(
            "이 파일 경로에서 Git 리포지토리를 찾지 못했습니다.\n"
            f"파일: {file_path}\n"
            f"에러: {repo_root_res.stderr.strip()}"
        )
    repo_root = Path(repo_root_res.stdout.strip())

    # 파일이 리포 내부인지 확인
    try:
        rel_file_path = file_path.relative_to(repo_root)
    except ValueError:
        raise RuntimeError(
            f"파일이 리포지토리 외부에 있습니다.\n"
            f"리포 루트: {repo_root}\n파일: {file_path}"
        )

    # 2) origin remote 확인
    origin_res = _run(["git", "remote", "get-url", "origin"], cwd=repo_root)
    if origin_res.returncode != 0:
        raise RuntimeError(
            "Git remote 'origin'이 설정되어 있지 않습니다.\n"
            f"Repository: {repo_root}\n"
            "다음 명령으로 origin을 추가하세요:\n"
            "  git remote add origin <repository-url>"
        )
    origin_url = origin_res.stdout.strip()
    if not is_github_repo_public(origin_url):
        print("이 레포지토리는 비공개이거나 존재하지 않습니다.")
        return 

    # 3) 기본 브랜치 탐지 (origin/HEAD → origin/<default>)
    def _detect_default_branch() -> Optional[str]:
        # 방법 A: symbolic-ref
        a = _run(["git", "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"], cwd=repo_root)
        if a.returncode == 0:
            val = a.stdout.strip()      # e.g., "origin/main"
            if "/" in val:
                return val.split("/", 1)[1]

        # 방법 B: remote show origin
        b = _run(["git", "remote", "show", "origin"], cwd=repo_root)
        if b.returncode == 0:
            m = re.search(r"HEAD branch:\s+([^\s]+)", b.stdout)
            if m:
                return m.group(1)

        return None

    default_branch = _detect_default_branch()
    # 최후수단: main → master 순으로 시도
    candidate_branches = [b for b in [default_branch, "main", "master"] if b]

    # 4) git add
    add_res = _run(["git", "add", str(rel_file_path)], cwd=repo_root)
    if add_res.returncode != 0:
        raise RuntimeError(f"git add 실패:\n{add_res.stderr}")

    # 5) 변경 사항이 있는지 확인 (staged 기준)
    # 특정 파일만 대상으로 조용히(quiet) 체크
    diff_cached = _run(["git", "diff", "--cached", "--quiet", "--", str(rel_file_path)], cwd=repo_root)
    has_staged_change = diff_cached.returncode == 1  # 0: 변경 없음, 1: 변경 있음, 2: 에러

    # 6) commit (필요할 때만)
    if has_staged_change:
        commit_msg = f"{rel_file_path.name} 파일 자동 추가/업데이트"
        commit_res = _run(["git", "commit", "-m", commit_msg], cwd=repo_root)
        if commit_res.returncode != 0:
            raise RuntimeError(f"git commit 실패:\n{commit_res.stderr}")
    # 변경 없으면 커밋 생략

    # 7) push (기본 브랜치 후보 순회)
    last_err = None
    for br in candidate_branches:
        push_res = _run(["git", "push", "origin", br], cwd=repo_root)
        if push_res.returncode == 0:
            default_branch = br
            break
        last_err = push_res.stderr
    else:
        # 모든 후보 브랜치 push 실패
        raise RuntimeError(
            "git push 실패: 기본 브랜치를 찾거나 푸시하지 못했습니다.\n"
            f"시도한 브랜치: {candidate_branches}\n"
            f"마지막 오류:\n{(last_err or '').strip()}\n\n"
            "가능한 원인:\n"
            "1) 인증 문제: GitHub 토큰/SSH 키 자격 증명 확인\n"
            "2) 권한 문제: repository 쓰기 권한\n"
            "3) 브랜치 문제: 원격 브랜치 존재 여부 또는 보호 규칙"
        )

    # 8) 웹 URL 생성 (SSH/HTTPS 모두 대응해서 https://github.com/owner/repo 형태로 통일)
    def _to_https_web_url(remote: str) -> Optional[str]:
        remote = remote.strip()
        if remote.endswith(".git"):
            remote = remote[:-4]

        # SSH: git@github.com:owner/repo
        m = re.match(r"git@([^:]+):(.+)$", remote)
        if m:
            host = m.group(1)
            path = m.group(2)
            return f"https://{host}/{path}"

        # HTTPS: https://github.com/owner/repo
        if remote.startswith("http://") or remote.startswith("https://"):
            return remote

        return None

    web_base = _to_https_web_url(origin_url)
    if not web_base:
        # 웹 URL로 바꾸지 못하면 리포 루트 경로와 origin을 알려주고 종료
        raise RuntimeError(
            "origin URL을 웹 URL로 변환하지 못했습니다.\n"
            f"origin: {origin_url}\n"
            "GitHub(또는 호환 호스트) 원격인지 확인하세요."
        )

    web_url = f"{web_base}/blob/{default_branch}/{str(rel_file_path).replace(os.sep, '/')}"
    print("깃허브 파일 업로드 완료!!")
    return web_url



def is_github_repo_public(repo_url: str) -> bool:
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", repo_url)
    if not m:
        raise ValueError("유효한 GitHub URL이 아닙니다.")
    owner, repo = m.group("owner"), m.group("repo")

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(api_url)
    
    if resp.status_code == 200:
        data = resp.json()
        return not data.get("private", True)
    elif resp.status_code == 404:
        # 접근 불가 = 비공개이거나 존재하지 않음
        return False
    else:
        raise RuntimeError(f"API 오류: {resp.status_code}")
    

    