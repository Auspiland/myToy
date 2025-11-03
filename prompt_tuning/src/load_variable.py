import json

def count_id():
    with open(r"C:\Users\T3Q\jeonghan\my_github\myToy\prompt_tuning\src\variable.json", "r+", encoding="utf-8") as f:
        data = json.load(f)           # 기존 데이터 읽기
        id_count = data["id_count"]   # 현재 ID
        data["id_count"] += 1         # 증가

        f.seek(0)                     # 파일 처음으로 이동
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()                  # 이전 내용이 남지 않도록 잘라냄

    return id_count
