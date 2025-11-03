import json
from pathlib import Path
from datetime import datetime


def jsonl_to_comparison_md(jsonl_path: str, output_md_path: str = None):
    """
    JSONL 파일을 읽어서 프롬프트별 답변 비교 분석을 위한 MD 파일로 변환합니다.

    Args:
        jsonl_path: 입력 JSONL 파일 경로
        output_md_path: 출력 MD 파일 경로 (기본값: 입력 파일명_comparison.md)
    """
    # 파일 경로 처리
    jsonl_path = Path(jsonl_path)
    if output_md_path is None:
        output_md_path = jsonl_path.parent / f"{jsonl_path.stem}_comparison.md"
    else:
        output_md_path = Path(output_md_path)

    # JSONL 파일 읽기
    results = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 빈 줄 제외
                results.append(json.loads(line))

    # MD 파일 생성
    with open(output_md_path, 'w', encoding='utf-8') as f:
        # 헤더
        f.write("# 프롬프트 답변 비교 분석\n\n")
        f.write(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"총 {len(results)}개의 결과\n\n")
        f.write("---\n\n")

        # 목차
        f.write("## 목차\n\n")
        for i, result in enumerate(results, 1):
            prompt_summary = result.get('system_prompt', '').strip()[:50].replace('\n', ' ')
            if not prompt_summary:
                prompt_summary = "No system prompt"
            f.write(f"{i}. [결과 {result.get('id', i)}](#결과-{result.get('id', i)}): {prompt_summary}...\n")
        f.write("\n---\n\n")

        # 각 결과 상세
        for i, result in enumerate(results, 1):
            result_id = result.get('id', i)
            f.write(f"## 결과 {result_id}\n\n")

            # 기본 정보
            f.write("### 메타 정보\n\n")
            f.write(f"- **ID**: {result_id}\n")
            f.write(f"- **Task**: {result.get('task', 'N/A')}\n")

            # Arguments 정보
            if 'arguements' in result:
                f.write(f"- **Arguments**:\n")
                for key, value in result['arguements'].items():
                    f.write(f"  - {key}: `{value}`\n")
            f.write("\n")

            # System Prompt
            f.write("### System Prompt\n\n")
            system_prompt = result.get('system_prompt', '').strip()
            if system_prompt:
                f.write("```\n")
                f.write(system_prompt)
                f.write("\n```\n\n")
            else:
                f.write("*No system prompt*\n\n")

            # User Prompt
            f.write("### User Prompt\n\n")
            user_prompt = result.get('user_prompt', '').strip()
            if user_prompt:
                f.write("```\n")
                f.write(user_prompt)
                f.write("\n```\n\n")
            else:
                f.write("*No user prompt*\n\n")

            # Response
            f.write("### Response\n\n")
            response = result.get('response', '').strip()
            if response:
                f.write(response)
                f.write("\n\n")
            else:
                f.write("*No response*\n\n")

            # 구분선
            f.write("---\n\n")

        # 비교 섹션
        f.write("## 전체 비교 요약\n\n")
        f.write("### 프롬프트 비교\n\n")
        f.write("| ID | System Prompt | User Prompt | Task |\n")
        f.write("|---|---|---|---|\n")
        for result in results:
            result_id = result.get('id', 'N/A')
            system_snippet = result.get('system_prompt', '').strip()[:50].replace('\n', ' ').replace('|', '\\|')
            user_snippet = result.get('user_prompt', '').strip()[:50].replace('\n', ' ').replace('|', '\\|')
            task = result.get('task', 'N/A')
            f.write(f"| {result_id} | {system_snippet}... | {user_snippet}... | {task} |\n")

        f.write("\n### 답변 길이 비교\n\n")
        f.write("| ID | 답변 길이 (글자) | 답변 길이 (단어) |\n")
        f.write("|---|---|---|\n")
        for result in results:
            result_id = result.get('id', 'N/A')
            response = result.get('response', '')
            char_count = len(response)
            word_count = len(response.split())
            f.write(f"| {result_id} | {char_count:,} | {word_count:,} |\n")

        f.write("\n")

    print(f"[완료] MD 파일이 생성되었습니다: {output_md_path}")
    return output_md_path


if __name__ == "__main__":
    # 예시 사용
    input_file = r"C:\Users\T3Q\jeonghan\my_github\myToy\prompt_tuning\output\result.jsonl"
    output_file = r"C:\Users\T3Q\jeonghan\my_github\myToy\prompt_tuning\output\result_comparison.md"

    jsonl_to_comparison_md(input_file, output_file)
