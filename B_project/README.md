# B_project

알고리즘 및 코딩 테스트 관련 프로젝트입니다.

<!-- AUTO-UPDATE:START -->
<!-- 이 섹션은 GitHub Actions에 의해 자동으로 업데이트됩니다 -->
## 프로젝트 구성

### boj_bible
백준 알고리즘 문제 해결을 위한 파이썬 라이브러리입니다.

- **basic**: 기본 자료구조 (스택, 큐, 링크드 리스트, Union-Find, Heap)
- **graph**: 그래프 알고리즘 (BFS, DFS, 최단경로, 위상정렬)
- **tree**: 트리 알고리즘 (세그먼트 트리, LCA)
- **string**: 문자열 알고리즘 (패턴 매칭, Trie)
- **advanced**: 고급 알고리즘 (네트워크 플로우)

### CT (Coding Test)
코딩 테스트 자동화 및 기록 관련 도구입니다.

- 변경 사항(요약): B_project/CT/auto_solve/common_utils.py에서 LLM 관련 함수들의 기본 모델 파라미터가 "gpt-5"에서 "gpt-5-nano"로 변경되었습니다.
  - 영향을 받는 함수: response_GPT, response_GPT_stream, response_GPT_with_stream_fallback
  - 영향: model 인자를 생략하고 호출하던 기존 코드들은 이제 기본적으로 "gpt-5-nano"를 사용하게 됩니다. 특정 모델(예: gpt-5)을 계속 사용하려면 model 파라미터를 명시적으로 지정하세요.

사용 예시 (Python):
```python
from B_project.CT.auto_solve.common_utils import (
    response_GPT,
    response_GPT_stream,
    response_GPT_with_stream_fallback,
)

# 기본 사용: model 파라미터를 지정하지 않으면 'gpt-5-nano'가 사용됩니다.
text = response_GPT(system_prompt="시스템 메시지", user_prompt="사용자 질문")
print(text)

# 모델을 명시적으로 지정하려면:
text = response_GPT(system_prompt="", user_prompt="질문 내용", model="gpt-5")
print(text)

# 스트리밍 사용 예시:
for chunk in response_GPT_stream([{"role": "user", "content": "스트리밍 테스트"}]):
    print(chunk)

# 스트리밍 폴백을 사용하는 호출 예시:
result = response_GPT_with_stream_fallback(user_prompt="입력", max_retries=2, fallback_stream=True)
print(result)
```

주의 사항:
- 기본 모델 변경은 응답 지연, 응답 품질, 비용에 영향을 줄 수 있습니다. 필요에 따라 model 인자를 명시하여 원하는 모델을 사용하세요.
- 이 README의 나머지 부분(알고리즘 목록 등)은 변경되지 않았습니다.
<!-- AUTO-UPDATE:END -->

---



<!-- LAST_PROCESSED_SHA: none -->

<!-- LAST_PROCESSED_SHA: 990dd5cd59685b2c405fd0f22d02fd6ab5e1c65e -->
