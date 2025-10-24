from typing import Any, Tuple, Dict, List
import json, time, traceback
import ast

def normalize(value):
    # 1) 문자열인 경우
    if isinstance(value, str):
        # 숫자 문자열 → int/float 변환 시도
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        # 딕셔너리나 리스트 형태 문자열 파싱
        try:
            return ast.literal_eval(value)
        except Exception:
            return value.strip()  # 순수 문자열일 경우
    return value

def deep_equal(a, b):
    a_norm = normalize(a)
    b_norm = normalize(b)

    # list 내부 요소도 재귀적으로 비교
    if isinstance(a_norm, list) and isinstance(b_norm, list):
        return all(deep_equal(x, y) for x, y in zip(a_norm, b_norm)) and len(a_norm) == len(b_norm)

    # dict 내부 값도 재귀적으로 비교
    if isinstance(a_norm, dict) and isinstance(b_norm, dict):
        if set(a_norm.keys()) != set(b_norm.keys()):
            return False
        return all(deep_equal(a_norm[k], b_norm[k]) for k in a_norm)

    # 숫자 비교 (int vs float 허용)
    if isinstance(a_norm, (int, float)) and isinstance(b_norm, (int, float)):
        return float(a_norm) == float(b_norm)

    # 기본 비교
    return a_norm == b_norm

def evaluate_jsonl(jsonl_path: str, solution, score_fn=None, log_correct=False):
    """
    필수 기능만 담은 슬림 버전:
    - input: list/tuple → *args, dict → **kwargs
             str이면 json.loads 한 번만 시도하여 위 규칙 적용
    - answer: str이면 json.loads 한 번 시도(실패시 원문 유지)
    - score_fn 없으면 == 비교
    """
    total, correct, fails = 0, 0, []
    times = []

    def parse_input(v: Any) -> Tuple[List[Any], Dict[str, Any]]:
        # 문자열이면 JSON 파싱 한 번만 시도
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except Exception:
                pass  # 그대로 둠(스칼라면 단일 인자 취급)
        if isinstance(v, dict):
            return [], v
        if isinstance(v, (list, tuple)):
            return list(v), {}
        # 스칼라 단건
        return [v], {}

    def parse_answer(v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return v
        return v

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)

            raw_in = rec.get("input", [])
            args, kwargs = parse_input(raw_in)
            truth = parse_answer(rec.get("answer", None))
            note = rec.get("note", "")
            tags = rec.get("tags", []) or []

            try:
                t0 = time.perf_counter()
                # 형태에 맞게 한 번만 호출
                pred = solution(*args, **kwargs)
                dt = time.perf_counter() - t0
                times.append(dt)

                ok = bool(score_fn(pred, truth)) if score_fn else (pred == truth)
                if ok:
                    correct += 1
                    if log_correct:
                        print(f"✅ {total+1:03d} | {dt*1000:.2f}ms | 입력={raw_in} → 출력={pred}")
                else:
                    raw_in_rec = json.dumps(raw_in)[:300]
                    fails.append((raw_in_rec, truth, pred, note, tags, dt))
            except Exception as e:
                raw_in_rec = json.dumps(raw_in)[:300]
                fails.append((raw_in, truth, f"Exception: {e}\n{traceback.format_exc()}", note, ["err"], 0.0))
            total += 1

    avg = (sum(times)/len(times))*1000 if times else 0.0
    print("\n--- 요약 ---")
    rate = (correct/total*100) if total else 0.0
    print(f"총 {total}건 중 {correct}건 정답 ({rate:.1f}%)")
    print(f"평균 실행시간: {avg:.6f}ms")
    print(times[-1])

    if fails:
        print(f"\n❌ 틀린 {len(fails)}건 목록:")
        for i, (inp, truth, pred, note, tags, dt) in enumerate(fails, 1):
            print(f"[{i}] 입력: {inp}\n예상: {truth}\n출력: {pred}\n시간: {dt*1000:.2f}ms\ntags: {tags}\nnote: {note}\n---")

    return {
        "total": total,
        "correct": correct,
        "fails": fails,
        "avg_total_ms": avg
    }

def find_bad_line(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                s = line.rstrip("\n")
                pos = e.pos  # 0-based
                L = max(0, pos-20); R = min(len(s), pos+20)
                ctx = s[L:R]
                caret = " "*(pos-L) + "^"
                print(f"[에러] line={ln}, col={e.colno}, char(pos)={e.pos}")
                print(ctx)
                print(caret)
                print("원문 repr:", repr(s))
                return
    print("모든 라인 OK")
