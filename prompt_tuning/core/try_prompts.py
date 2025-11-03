import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from src.common_utils import response_GPT
from src.load_variable import count_id

SYSTEM_PROMPT = """
You are a professional reviewer of code.
"""

USER_PROMPT = """
Summary the following code.
After summarizing, translate the summary in korean.
"""

file_path = r"C:\Users\T3Q\jeonghan\my_github\myToy\prompt_tuning\data\rect2region_fast_v2.py"

with open(file_path, "r", encoding="utf-8") as f:
    code_str = f.read()

code_str = "Code content:\n" + code_str

messages=[
    {"role":"system","content":SYSTEM_PROMPT},
    {"role":"user","content":code_str},
    {"role":"user","content":USER_PROMPT}
]

print("Requesting GPT ...", flush=True)
res = response_GPT(messages=messages, model="gpt-5-mini")
print("="*50)

print(res)

result = {
    "id": count_id(),
    "system_prompt" : SYSTEM_PROMPT,
    "user_prompt" : USER_PROMPT,
    "task" : "summarize python code",
    "arguements" : {
        "file_path" : file_path
    },
    "response": res
}

with open(r"C:\Users\T3Q\jeonghan\my_github\myToy\prompt_tuning\output\result.jsonl", 'a', encoding="utf-8") as f:
    f.write(json.dumps(result, ensure_ascii=False) + "\n")