import os, sys
import json
import time
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from schema.kafka_schema import youtube_script_schema as schema

source = r"./download_folder/PL9a4x_yPK_86-3n5ggM7jescX0Q4770iU"
temp_target = r"./download_folder/temp"
target = r"./spark/data/test_json"

# 대상 디렉토리가 없으면 생성
os.makedirs(temp_target, exist_ok=True)
os.makedirs(target, exist_ok=True)

keys = [field.name for field in schema.fields]

print("Start throwing")
for filename in os.listdir(source):
    print("Go!")
    if filename.endswith(".txt"):
        txt_path = os.path.join(source, filename)
        temp_path = os.path.join(temp_target, filename.replace(".txt", ".json"))
        json_path = os.path.join(target, filename.replace(".txt", ".json"))

        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) < len(keys):
            raise ValueError(f"라인 수가 부족합니다: {len(lines)}줄 / 필드 {len(keys)}개")
 
        # 예시: 한 줄씩 json 객체로 나누기 (또는 전체 내용 하나로 처리해도 됨)
        json_data = {key: value.strip('\n') for key, value in zip(keys, lines)}


        # JSON으로 저장
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)

        # 완료 후 원자적으로 이동 (Spark가 감지할 수 있게)
        shutil.move(temp_path, json_path)

        print(f"✅ {filename} → {os.path.basename(json_path)} 변환 완료")
    time.sleep(3)






print("--Throwing End!--")
print("Waiting...")
time.sleep(30)

for filename in os.listdir(target):
    file_path = os.path.join(target, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
print("Reset successed!")