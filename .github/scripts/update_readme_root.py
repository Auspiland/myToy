#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
myToy 루트 README 자동 업데이트 스크립트

각 프로젝트의 README를 분석하여 루트 README에 간략한 프로젝트 목록을 자동 생성합니다.
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

def calc_changed_files(base_sha: str, head_sha: str, project_dirs: List[str]) -> List[str]:
    if base_sha == head_sha:
        return []
    changed = []
    for pdir in project_dirs:
        readme_path = f"{pdir}/README.md"
        try:
            diff_out = run(["git", "diff", "--name-only", f"{base_sha}..{head_sha}", "--", readme_path])
            if diff_out.strip():
                changed.append(readme_path)
        except subprocess.CalledProcessError:
            continue
    return changed

def read_project_readmes(project_dirs: List[str]) -> str:
    content = []
    for pdir in project_dirs:
        readme_path = Path(pdir) / "README.md"
        if readme_path.exists():
            text = readme_path.read_text(encoding="utf-8")
            # 첫 200줄만 읽기 (간략한 요약용)
            lines = text.splitlines()[:200]
            content.append(f"\n### {pdir}/README.md (처음 200줄)\n```markdown\n")
            content.append("\n".join(lines))
            content.append("\n```\n")
    return "\n".join(content)

# -----------------------------
# LLM call
# -----------------------------

@retry(wait=wait_exponential(multiplier=1, min=2, max=20), stop=stop_after_attempt(4))
def llm_summarize(openai_key: str, model: str, prompt: str) -> str:
    client = OpenAI(api_key=openai_key)

    token_param = {"max_output_tokens": 3000}

    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "You are a technical documentation expert specializing in creating concise project summaries."},
            {"role": "user", "content": prompt}
        ],
        **token_param
    )
    return resp.output_text

# -----------------------------
# Main
# -----------------------------

TEMPLATE = """myToy 루트 README 자동 업데이트

## 저장소 정보
- myToy: 여러 독립적인 토이 프로젝트들의 모노레포
- 프로젝트: geo_map, Mini-Pipeline, B_project 및 기타 파일들

## 작성 지침
각 프로젝트를 읽고 다음 형식으로 간략하게 요약:

## [프로젝트명]
- **설명**: 프로젝트가 하는 일 (한 줄)
- **기술**: 주요 기술 스택
- **특징**: 핵심 기능 2-3개

## 프로젝트 README 요약 (처음 200줄)
{project_summaries}

## 출력 요구사항
- 한국어로 작성
- 각 프로젝트당 3-4줄로 간결하게
- 최대 200줄 이내
- AUTO-UPDATE 마커 사이에 들어갈 마크다운만 출력
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme", required=True)
    ap.add_argument("--llm-model", default=os.getenv("LLM_MODEL", "gpt-5-mini"))
    ap.add_argument("--section-start", required=True)
    ap.add_argument("--section-end", required=True)
    ap.add_argument("--last-sha-start", required=True)
    ap.add_argument("--last-sha-end", default="-->")
    ap.add_argument("--project-dirs", required=True, help="Comma-separated list of project directories")
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

    project_dirs = [p.strip() for p in args.project_dirs.split(",")]

    changed = calc_changed_files(base_sha, head_sha, project_dirs)
    if not changed:
        print("No project README changes detected. Skipping LLM call.")
        updated = upsert_marker(readme_txt, args.last_sha_start, args.last_sha_end, head_sha)
        if updated != readme_txt:
            readme_path.write_text(updated, encoding="utf-8")
        return

    print(f"Detected changes in {len(changed)} project README(s). Proceeding with LLM analysis...")

    project_summaries = read_project_readmes(project_dirs)

    prompt = TEMPLATE.format(
        base_sha=base_sha,
        head_sha=head_sha,
        project_summaries=project_summaries or "No project READMEs found."
    )

    content = llm_summarize(openai_key, args.llm_model, prompt).strip()

    readme_new = replace_between(readme_txt, args.section_start, args.section_end, content)
    readme_new = upsert_marker(readme_new, args.last_sha_start, args.last_sha_end, head_sha)

    if readme_new != readme_txt:
        Path(readme_path).write_text(readme_new, encoding="utf-8")
        print("Root README updated.")
    else:
        print("Root README unchanged.")

if __name__ == "__main__":
    main()
