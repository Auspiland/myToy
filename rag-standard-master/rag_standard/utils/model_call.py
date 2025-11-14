from typing import List, Dict, Any
import requests
from openai import OpenAI
from openai.resources.chat.completions import CompletionsWithStreamingResponse
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
import os
from rag_standard.utils.config_setting import load_env 

load_env()

LLM_URL = os.getenv('LLM_URL')
TEXT_EMBEDDING_API_URL = os.getenv('TEXT_EMBEDDING_API_URL')

def embed_text(texts: List[str]) -> List[List[float]]:
    """
    텍스트 임베딩 함수
    """

    input_data = {
            "text": texts,  # 문장 리스트
            "mode": "dense"  # 또는 "sparse", "dense+sparse" 등 필요 시
    }

    r = requests.post(TEXT_EMBEDDING_API_URL, json=input_data)
    return r.json()[0]

def generate_llm_response(system_prompt: str, user_prompt: str, stream: bool = False, temperature: float = 0.7, top_p: float = 0.8, top_k: int = 20, repetition_penalty: float = 1.05, extra_body: Dict[str, Any] = {}) -> str:
    """
    LLM 응답 생성 함수
    """

    client = OpenAI(
        api_key="EMPTY",
        base_url=LLM_URL
    )
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model='qwen-2.5',
        messages=messages,
        stream=stream,
        temperature=temperature,
        top_p=top_p,
        extra_body= {
        'top_k': top_k,
        'repetition_penalty': repetition_penalty,
        **extra_body
        }
    )

    if stream:
        return response

    return response.choices[0].message.content