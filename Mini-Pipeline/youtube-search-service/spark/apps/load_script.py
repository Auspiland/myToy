from schema.kafka_schema import youtube_script_schema
import os

base_path = "/app/data"

def load_script(spark, channel_code, max_video =100000):

    folder_path = os.path.join(base_path,channel_code)
    if not os.path.exists(folder_path):
        raise ValueError("This folder is not exist. Please check you Channel code. :",folder_path)

    records = []
    expected_fields = 10  # youtube_script_schema의 필드 수
    count=0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) < expected_fields:
                    print(f"[경고] {filename}: 줄 수 부족 ({len(lines)}줄)")
                    print(lines)
                    continue
                row = tuple(lines[:expected_fields])  # 정확히 10줄만 사용
                records.append(row)
        count+=1
        if count >= max_video:
            break

    df = spark.createDataFrame(records, schema=youtube_script_schema)
    return df