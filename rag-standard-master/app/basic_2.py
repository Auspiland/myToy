import requests

# 빠른 테스트
def quick_embedding_test():
    url = "http://localhost:8502/search/hybrid"
    
    # 임베딩 생성
    response = requests.post(url, json={
        "user_query": "기기냉각수계통의 지원받는 계통 모두 알려줘 "
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"성공!")
        return result
    else:
        print(f"에러: {response.status_code}")
        print(response.text)

response = quick_embedding_test()

from openai import OpenAI

llm = OpenAI(
    api_key="EMPTY", 
    base_url="http://133.186.220.141:8080/qwen3-32b/v1"
)

user_prompt = f'''
## 사용자 질문:
주급수 계통의 구성기기에 대해서 알려줘

## 참고 문서:
{response.text}

## 답변:
'''


response = llm.chat.completions.create(
    model="qwen3-32b",
    messages=[{"role": "system", "content": '너는 한국수력원자력 회사의 AI 비서이다. 사용자의 질문에 대해 문서를 참고하여 친절하고 정확하게 답변해야 한다.'},
        {"role": "user", "content": user_prompt}],
    extra_body={
        "chat_template_kwargs": {"enable_thinking": False},
    },
    stream=True
)

# print(response.choices[0].message.content)

generated_text = ''

try:
    for chunk in response:
        try:
            generated_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content,end='')
        except:
            pass
    #return completion.choices[0].message.content
finally:
    response.close()
