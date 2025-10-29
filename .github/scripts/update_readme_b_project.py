#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B_project README 자동 업데이트 스크립트

Git diff를 분석하여 LLM을 통해 B_project/README.md의 자동 업데이트 섹션을 갱신합니다.
"""

import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple

from tenacity import retry, stop_after_attempt, wait_exponential

from openai import OpenAI

# -----------------------------
# Helpers
# -----------------------------

def run(cmd: List[str]) -> str:
    out = subprocess.check_output(cmd, text=True).strip()
    return out

def get_current_sha() -> str:
    return run(["git", "rev-parse", "HEAD"])

def extract_marker(text: str, start_mark: str, end_mark: str) -> str | None:
    pat = re.escape(start_mark) + r"\s*([0-9a-f]{7,40})\s*" + re.escape(end_mark)
    m = re.search(pat, text)
    return m.group(1) if m else None

def upsert_marker(text: str, start_mark: str, end_mark: str, sha: str) -> str:
    pat = re.escape(start_mark) + r"\s*([0-9a-f]{7,40})\s*" + re.escape(end_mark)
    repl = f"{start_mark} {sha} {end_mark}"
    if re.search(pat, text):
        return re.sub(pat, repl, text)
    else:
        return text.rstrip() + "\n\n" + repl + "\n"

def slice_between(text: str, start_mark: str, end_mark: str) -> Tuple[int, int]:
    s = text.find(start_mark)
    e = text.find(end_mark)
    if s == -1 or e == -1 or e <= s:
        return (-1, -1)
    return (s + len(start_mark), e)

def replace_between(text: str, start_mark: str, end_mark: str, new_content: str) -> str:
    s, e = slice_between(text, start_mark, end_mark)
    if s == -1:
        return text.rstrip() + f"\n\n{start_mark}\n{new_content}\n{end_mark}\n"
    return text[:s] + "\n" + new_content.strip() + "\n" + text[e:]

def calc_changed_files(target_dir: str, base_sha: str, head_sha: str) -> List[str]:
    if base_sha == head_sha:
        return []
    diff_out = run(["git", "diff", "--name-only", f"{base_sha}..{head_sha}", "--", target_dir])
    files = [f for f in diff_out.splitlines()
             if f.strip() and not f.startswith('.github/') and not f.endswith('README.md')]
    return files

def collect_diffs(files: List[str], base_sha: str, head_sha: str, max_bytes: int) -> str:
    chunks = []
    used = 0
    for f in files:
        diff_txt = run(["git", "diff", f"{base_sha}..{head_sha}", "--", f])
        if not diff_txt:
            continue
        header = f"\n### {f}\n```\n"
        footer = "\n```\n"
        piece = header + diff_txt + footer
        b = len(piece.encode("utf-8"))
        if used + b > max_bytes:
            remain = max_bytes - used
            if remain > 1024:
                piece = (header + diff_txt)[:remain] + "\n```\n"
                chunks.append(piece)
                used = max_bytes
            break
        chunks.append(piece)
        used += b
    return "\n".join(chunks).strip()

# -----------------------------
# LLM call
# -----------------------------

@retry(wait=wait_exponential(multiplier=1, min=2, max=20), stop=stop_after_attempt(4))
def llm_summarize(openai_key: str, model: str, prompt: str) -> str:
    client = OpenAI(api_key=openai_key)

    token_param = {"max_output_tokens": 6000}

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "You are a technical documentation expert specializing in algorithm libraries and competitive programming."},
            {"role": "user", "content": prompt}
        ],
        **token_param
    )
    return resp.output_text

# -----------------------------
# Main
# -----------------------------

TEMPLATE = """B_project README 자동 업데이트

## 프로젝트 정보
- 알고리즘 및 코딩 테스트 관련 프로젝트
- 구성: boj_bible (백준 알고리즘 라이브러리), CT (코딩 테스트 자동화)
- 기술: Python, Data Structures, Algorithms

## 핵심 원칙
1. **기존 구조 유지**: 섹션 구조, 제목, 순서를 변경하지 말 것
2. **변경된 부분만 수정**: diff에 나타난 변경사항과 직접 관련된 내용만 업데이트
3. **미변경 내용 보존**: diff에 없는 부분은 현재 내용을 그대로 복사

## 현재 README 내용
```markdown
{current_content}
```

## 코드 변경사항 (diff)
{diff}

## 업데이트 지침
- 알고리즘 추가/수정 → 알고리즘 목록 업데이트
- 모듈 구조 변경 → 구조 섹션 업데이트
- API 변경 → 사용 예시 업데이트
- 성능 개선 → 시간/공간복잡도 업데이트
- 테스트 추가 → 테스트 섹션 업데이트
- 중요 변경 → 버전 히스토리 추가

## 출력 요구사항
- 한국어로 작성
- 기술적으로 정확하게: 알고리즘명, 복잡도, 사용법 명시
- 코드 블록 사용: Python 예시 코드
- AUTO-UPDATE 마커 사이에 들어갈 마크다운만 출력
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-dir", required=True)
    ap.add_argument("--readme", required=True)
    ap.add_argument("--llm-model", default=os.getenv("LLM_MODEL", "gpt-5-mini"))
    ap.add_argument("--section-start", required=True)
    ap.add_argument("--section-end", required=True)
    ap.add_argument("--last-sha-start", required=True)
    ap.add_argument("--last-sha-end", default="-->")
    ap.add_argument("--max-diff-bytes", type=int, default=int(os.getenv("MAX_DIFF_BYTES", "80000")))
    args = ap.parse_args()

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    repo_root = Path(".").resolve()
    readme_path = repo_root / args.readme

    head_sha = get_current_sha()

    readme_txt = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    base_sha = extract_marker(readme_txt, args.last_sha_start, args.last_sha_end)
    if base_sha is None:
        try:
            base_sha = run(["git", "rev-parse", "HEAD~1"])
        except subprocess.CalledProcessError:
            base_sha = head_sha

    changed = calc_changed_files(args.target_dir, base_sha, head_sha)
    if not changed:
        print("No changes in target directory since last processed SHA. Skipping LLM call.")
        updated = upsert_marker(readme_txt, args.last_sha_start, args.last_sha_end, head_sha)
        if updated != readme_txt:
            readme_path.write_text(updated, encoding="utf-8")
        return

    print(f"Detected {len(changed)} changed file(s). Proceeding with LLM analysis...")

    diff_snippets = collect_diffs(changed, base_sha, head_sha, args.max_diff_bytes)

    current_section = ""
    s_idx, e_idx = slice_between(readme_txt, args.section_start, args.section_end)
    if s_idx != -1:
        current_section = readme_txt[s_idx:e_idx].strip()

    prompt = TEMPLATE.format(
        target_dir=args.target_dir,
        base_sha=base_sha,
        head_sha=head_sha,
        diff=diff_snippets or "No textual diff available.",
        current_content=current_section or "No existing auto-update section."
    )

    content = llm_summarize(openai_key, args.llm_model, prompt).strip()

    readme_new = replace_between(readme_txt, args.section_start, args.section_end, content)
    readme_new = upsert_marker(readme_new, args.last_sha_start, args.last_sha_end, head_sha)

    if readme_new != readme_txt:
        Path(readme_path).write_text(readme_new, encoding="utf-8")
        print("README updated.")
    else:
        print("README unchanged.")

if __name__ == "__main__":
    main()
