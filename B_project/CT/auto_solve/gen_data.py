# 목적: LLM에 "문제"를 그대로 보내, (1) 결과물 스키마 규정 → (2) 코너 케이스 분석 → (3) 입력 테스트 데이터 생성
# 조건: 내장 모듈만 사용, 환경변수로 API/KEY/MODEL 지정, 각 단계를 별도 호출.
# 주의: 0, 빈 리스트, max 범위 등 극단값 포함. 대규모 성능 케이스는 별도 size_class로 분리.

import re
import os, json, time, sys
import logging
from dotenv import load_dotenv
load_dotenv()

from common_utils import response_GPT, clean_filename, extract_json
log = logging.getLogger(__name__)


# --- 1) 결과물 스키마 규정 ---
def request_schema(problem_text: str) -> dict:
    sys_prompt = (
        "당신은 코딩테스트 데이터 생성 전문가입니다. "
        "출력은 반드시 JSON이어야 합니다."
    )
    user_prompt = f"""
다음 '문제'를 바탕으로 테스트 데이터의 결과물 스키마를 규정하세요.
요구:
- 1행(=1개 데이터) 단위 스키마를 JSON으로 정의합니다.
- 각 행에는 최소 다음 키를 포함해야 합니다:
  input: 문제 입력의 원시 표현(문자열 또는 JSON 직렬화 문자열)
  answer: 해당 입력의 정답(문자열 또는 JSON 직렬화 문자열)
  note: 케이스 의도/설명(간단)
  tags: ["corner" | "perf" 등 라벨 배열]
  size_class: "tiny"|"small"|"medium"|"large"|"xlarge"
- input/answer는 손실 없이 역직렬화 가능한 형태를 권장합니다.
- 데이터셋 전체 형태도 함께 제시합니다:
  dataset: {{"schema": <1행 스키마 JSON>, "format": "jsonl"}}

문제:
\"\"\"{problem_text}\"\"\"

반드시 다음 JSON을 출력:
{{
  "dataset": {{
    "schema": {{
      "input": "string",
      "answer": "string",
      "note": "string",
      "tags": ["string"],
      "size_class": "string"
    }},
    "format": "jsonl"
  }}
}}
"""
    content = response_GPT(
        messages=[{"role":"system","content":sys_prompt},
                  {"role":"user","content":user_prompt}],
        model="gpt-5-mini"
    )
    return extract_json(content)

# --- 2) 코너 케이스 예측 분석 ---
def request_corner_analysis(problem_text: str, dataset_schema: dict) -> dict:
    sys_prompt = (
        "당신은 코딩테스트의 코너 케이스 설계 전문가입니다. "
        "출력은 반드시 JSON."
    )
    user_prompt = f"""
'문제'에 대해 코너 케이스를 체계적으로 분석하세요.
요구:
- 입력 도메인/제약을 근거로 케이스 분류 기준을 제시합니다.
- 각 분류에 대해 최소/최대/빈/동일값/정렬/역정렬/중복/음수/0/오버플로 인접 등을 포괄합니다.
- 시간복잡도 관점의 위험 케이스도 포함합니다(예: 최악 분포, 해시 충돌 유사, 병합 경계 등).
- 결과는 JSON으로, 분류 목록과 각 분류별 설명/예시 입력 템플릿을 담습니다.

dataset 1행 스키마(참고용):
{json.dumps(dataset_schema.get("dataset", {}).get("schema", {}), ensure_ascii=False)}

문제:
\"\"\"{problem_text}\"\"\"

반드시 다음 JSON을 출력:
{{
  "classes": [
    {{
      "name": "string",
      "rationale": "string",
      "examples": ["입력 형식 예시 문자열들(직렬화)"]
    }}
  ]
}}
"""
    content = response_GPT(
        messages=[{"role":"system","content":sys_prompt},
                  {"role":"user","content":user_prompt}]
    )
    return extract_json(content)

# --- 3) 입력 테스트 데이터 생성 (corner + perf) ---
# 목적: corner 데이터 생성과 perf 데이터 생성을 분리
# 조건: 내장 모듈만 사용, 기존 response_GPT / extract_json 재사용 가정
import json

def request_corner_test_data(problem_text: str, dataset_schema: dict, corner_plan: dict, n_corner=40, special_prompt="") -> dict:
    sys_prompt = (
        "당신은 코딩테스트 벤치마크 데이터 생성기입니다. "
        "출력은 반드시 JSON. 실제 사용 가능한 jsonl 레코드를 생성하세요."
    )
    special_prompt = "다음을 유의:\n" + special_prompt if special_prompt else ""
    user_prompt = f"""
'문제'에 대해 corner 테스트 데이터를 생성하세요.

요구:
- dataset 1행 스키마 준수: {json.dumps(dataset_schema.get("dataset", {}).get("schema", {}), ensure_ascii=False)}
- 총 레코드 수: 약 {n_corner}개
- 각 레코드는 JSONL 한 줄로 serialize 가능해야 합니다.
- input/answer는 파싱 가능한 문자열(JSON 직렬화 문자열 권장).
- note에 케이스 의도, tags는 반드시 ["corner"] 만 포함.
- size_class는 tiny/small/medium 위주로 생성(필요 시 일부 medium까지).
{special_prompt}

분류/예시(참고용):
{json.dumps(corner_plan, ensure_ascii=False)}

문제:
\"\"\"{problem_text}\"\"\"

반드시 다음 JSON을 출력:
{{
  "records": [
    {{
      "input": list[Any],
      "answer": Any,
      "note": "string",
      "tags": ["corner"],
      "size_class": "tiny/small/medium 중 하나"
    }}
  ]
}}
"""
    log.info("Corner-data generating")
    content = response_GPT(
        messages=[{"role":"system","content":sys_prompt},
                  {"role":"user","content":user_prompt}]
    )
    out = extract_json(content)
    if not isinstance(out, dict): out = {"records":[]}
    if "records" not in out or not isinstance(out["records"], list): out["records"] = []
    # 안전 정규화
    norm = []
    for rec in out["records"]:
        if not isinstance(rec, dict): continue
        tags = rec.get("tags", ["corner"])
        if tags != ["corner"]: tags = ["corner"]
        sc = rec.get("size_class", "small")
        if sc not in ("tiny","small","medium"): sc = "small"
        norm.append({
            "input": rec.get("input", []),
            "answer": rec.get("answer", None),
            "note": rec.get("note", ""),
            "tags": tags,
            "size_class": sc,
        })
    return {"records": norm}

def request_perf_test_data(problem_text: str, dataset_schema: dict, n_perf=12, special_prompt="") -> dict:
    sys_prompt = (
        "당신은 코딩테스트 벤치마크 데이터 생성기입니다. "
        "출력은 반드시 JSON. 실제 사용 가능한 jsonl 레코드를 생성하세요."
    )
    special_prompt = "다음을 유의:\n" + special_prompt if special_prompt else ""
    user_prompt = f"""
'문제'에 대해 성능(perf) 테스트 데이터를 생성하세요.

요구:
- dataset 1행 스키마 준수: {json.dumps(dataset_schema.get("dataset", {}).get("schema", {}), ensure_ascii=False)}
- 총 레코드 수: 약 {n_perf}개
- 각 레코드는 JSONL 한 줄로 serialize 가능해야 합니다.
- input/answer는 파싱 가능한 문자열(JSON 직렬화 문자열 권장).
- note에 케이스 의도, tags는 반드시 ["perf"] 만 포함.
- size_class는 large/xlarge 위주로 생성.
- 최악 분포/시간복잡도 한계 근접/캐시 미스 유발/경계(0, 빈, max 인접) 포함하되, 답이 정의되는 입력만 생성.
- 가능한 크게 생성
- 입력 데이터 셋의 형태에 유의하며, "제한사항"을 잘 고려하세요.
{special_prompt}

문제:
\"\"\"{problem_text}\"\"\"

반드시 다음 JSON을 출력:
{{
  "records": [
    {{
      "input": list[Any],
      "answer": Any,
      "note": "string",
      "tags": ["perf"],
      "size_class": "large/xlarge 중 하나"
    }}
  ]
}}
"""
    log.info("Perf-data generating")
    content = response_GPT(
        messages=[{"role":"system","content":sys_prompt},
                  {"role":"user","content":user_prompt}]
    )
    out = extract_json(content)
    if not isinstance(out, dict): out = {"records":[]}
    if "records" not in out or not isinstance(out["records"], list): out["records"] = []
    # 안전 정규화
    norm = []
    for rec in out["records"]:
        if not isinstance(rec, dict): continue
        tags = rec.get("tags", ["perf"])
        if tags != ["perf"]: tags = ["perf"]
        sc = rec.get("size_class", "large")
        if sc not in ("large","xlarge"): sc = "large"

        input_temp = rec.get("input", [])
        if isinstance(input_temp,list) and len(input_temp) == 1:
            input_temp = input_temp[0]
        answer_temp = rec.get("input", [])
        if isinstance(answer_temp,list) and len(answer_temp) == 1:
            answer_temp = answer_temp[0]
        norm.append({
            "input": input_temp,
            "answer": rec.get("answer", None),
            "note": rec.get("note", ""),
            "tags": tags,
            "size_class": sc,
        })
    return {"records": norm}

def request_test_data(problem_text: str, dataset_schema: dict, corner_plan: dict, n_corner=40, n_perf=6, special_prompt="") -> dict:
    c = request_corner_test_data(problem_text, dataset_schema, corner_plan, n_corner=n_corner, special_prompt=special_prompt.strip())
    p = request_perf_test_data(problem_text, dataset_schema, n_perf=n_perf, special_prompt=special_prompt.strip())
    recs = []
    recs.extend(c.get("records", []))
    recs.extend(p.get("records", []))
    return {"records": recs}

# --- 실행 예시 ---
def main(problem_text, title=None, special_prompt=None):
    log.info("=== Setting Schema ===")
    schema = request_schema(problem_text)
    log.info("=== Analyzing corner cases ===")
    corner = request_corner_analysis(problem_text, schema)
    log.info("=== Generating data ===")
    data   = request_test_data(problem_text, schema, corner, special_prompt=special_prompt)
    log.info("=== END ===")
    if not title:
        title = problem_text[:10].strip()
        title = clean_filename(title)
    # 결과 출력: schema/corner 요약 + jsonl 파일 저장
    log.info("# schema\n", json.dumps(schema, ensure_ascii=False, indent=2))
    log.info("# corner_plan\n", json.dumps(corner, ensure_ascii=False, indent=2))
    # jsonl 저장
    path = rf"C:\_mangojelly\Git-mytoy\myToy\B_project\CT\auto_solve\generated_data\{title}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for rec in data.get("records", []):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    log.info(f"# saved: {path}  (records={len(data.get('records', []))})")
    return path

if __name__ == "__main__":
    problem_text = '''
점심시간에 도둑이 들어, 일부 학생이 체육복을 도난당했습니다. 다행히 여벌 체육복이 있는 학생이 이들에게 체육복을 빌려주려 합니다. 학생들의 번호는 체격 순으로 매겨져 있어, 바로 앞번호의 학생이나 바로 뒷번호의 학생에게만 체육복을 빌려줄 수 있습니다. 예를 들어, 4번 학생은 3번 학생이나 5번 학생에게만 체육복을 빌려줄 수 있습니다. 체육복이 없으면 수업을 들을 수 없기 때문에 체육복을 적절히 빌려 최대한 많은 학생이 체육수업을 들어야 합니다.

전체 학생의 수 n, 체육복을 도난당한 학생들의 번호가 담긴 배열 lost, 여벌의 체육복을 가져온 학생들의 번호가 담긴 배열 reserve가 매개변수로 주어질 때, 체육수업을 들을 수 있는 학생의 최댓값을 return 하도록 solution 함수를 작성해주세요.

제한사항
전체 학생의 수는 2명 이상 30명 이하입니다.
체육복을 도난당한 학생의 수는 1명 이상 n명 이하이고 중복되는 번호는 없습니다.
여벌의 체육복을 가져온 학생의 수는 1명 이상 n명 이하이고 중복되는 번호는 없습니다.
여벌 체육복이 있는 학생만 다른 학생에게 체육복을 빌려줄 수 있습니다.
여벌 체육복을 가져온 학생이 체육복을 도난당했을 수 있습니다. 이때 이 학생은 체육복을 하나만 도난당했다고 가정하며, 남은 체육복이 하나이기에 다른 학생에게는 체육복을 빌려줄 수 없습니다.
입출력 예
n	lost	reserve	return
5	[2, 4]	[1, 3, 5]	5
5	[2, 4]	[3]	4
3	[3]	[1]	2
입출력 예 설명
예제 #1
1번 학생이 2번 학생에게 체육복을 빌려주고, 3번 학생이나 5번 학생이 4번 학생에게 체육복을 빌려주면 학생 5명이 체육수업을 들을 수 있습니다.

예제 #2
3번 학생이 2번 학생이나 4번 학생에게 체육복을 빌려주면 학생 4명이 체육수업을 들을 수 있습니다.

'''
    main(problem_text)
