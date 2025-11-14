# RAG Standard 프로젝트

## 목차

- [RAG Standard 프로젝트](#rag-standard-프로젝트)
  - [목차](#목차)
  - [1. 소개](#1-소개)
    - [1.1. 프로젝트 목표](#11-프로젝트-목표)
    - [1.2. 핵심 기능](#12-핵심-기능)
  - [2. 프로젝트 구조](#2-프로젝트-구조)
  - [3. 설정 및 설치](#3-설정-및-설치)
    - [3.1. 사전 준비 사항](#31-사전-준비-사항)
    - [3.2. 저장소 복제](#32-저장소-복제)
    - [3.3. 환경 설정](#33-환경-설정)
      - [3.3.1. Python 가상 환경](#331-python-가상-환경)
      - [3.3.2. 의존성 설치](#332-의존성-설치)
    - [3.4. 환경 변수 (.env)](#34-환경-변수-env)
    - [3.5. OpenSearch 설정](#35-opensearch-설정)
  - [4. 데이터 처리 (Data Processing)](#4-데이터-처리-data-processing)
    - [4.1. 주요 기능](#41-주요-기능)
    - [4.2. 설정 및 실행](#42-설정-및-실행)
      - [4.2.1. 설정](#421-설정)
      - [4.2.2. 실행](#422-실행)
    - [4.3. 출력 구조](#43-출력-구조)
    - [4.4. 로깅](#44-로깅)
    - [4.5. 핵심 구성 요소 상세](#45-핵심-구성-요소-상세)
      - [4.5.1. 문서 로딩 (Loader)](#451-문서-로딩-loader)
      - [4.5.2. 임베딩 생성 (Embedding)](#452-임베딩-생성-embedding)
      - [4.5.3. 벡터 저장소 연동](#453-벡터-저장소-연동)
    - [4.6. 개발 및 사용자 정의](#46-개발-및-사용자-정의)
      - [4.6.1. 새로운 문서 로더 추가](#461-새로운-문서-로더-추가)
      - [4.6.2. 새로운 임베딩 모델 추가](#462-새로운-임베딩-모델-추가)
      - [4.6.3. 새로운 벡터 저장소 추가](#463-새로운-벡터-저장소-추가)
  - [5. RAG 워크플로우 (RAG Workflow)](#5-rag-워크플로우-rag-workflow)
    - [5.1. 워크플로우 설정 (YAML)](#51-워크플로우-설정-yaml)
      - [5.1.1. 주요 설정 파일: `naive_rag_workflow.yaml`](#511-주요-설정-파일-naive_rag_workflowyaml)
      - [5.1.2. `graph_settings`](#512-graph_settings)
      - [5.1.3. `tokenizer`](#513-tokenizer)
      - [5.1.4. `graph_node_config`](#514-graph_node_config)
      - [5.1.5. `evaluation_settings`](#515-evaluation_settings)
    - [5.2. RAG 파이프라인 실행](#52-rag-파이프라인-실행)
      - [5.2.1. 단일 질의 실행 (`scripts/run_graph_workflow.py`)](#521-단일-질의-실행-scriptsrun_graph_workflowpy)
      - [5.2.2. 대화형 CLI 채팅 (`scripts/cli_chat.py`)](#522-대화형-cli-채팅-scriptscli_chatpy)
    - [5.3. 평가 (`scripts/run_evaluation.py`)](#53-평가-scriptsrun_evaluationpy)
      - [5.3.1. QA 데이터셋 형식](#531-qa-데이터셋-형식)
      - [5.3.2. 평가 지표](#532-평가-지표)
      - [5.3.3. 결과 출력](#533-결과-출력)
    - [5.4. 핵심 구성 요소 상세](#54-핵심-구성-요소-상세)
      - [5.4.1. 그래프 워크플로우 (LangGraph)](#541-그래프-워크플로우-langgraph)
      - [5.4.2. 상태 (State)](#542-상태-state)
      - [5.4.3. 노드 (Node)](#543-노드-node)
      - [5.4.4. 그래프 빌드](#544-그래프-빌드)
    - [5.5. 토큰화](#55-토큰화)
    - [5.6. OpenSearch 연동](#56-opensearch-연동)
    - [5.7. LLM 연동](#57-llm-연동)
    - [5.8. 개발 및 사용자 정의](#58-개발-및-사용자-정의)
      - [5.8.1. 새로운 그래프 노드 추가](#581-새로운-그래프-노드-추가)
      - [5.8.2. 사용자 정의 그래프 빌더 생성](#582-사용자-정의-그래프-빌더-생성)
      - [5.8.3. 토크나이저 수정](#583-토크나이저-수정)
  - [6. 문제 해결](#6-문제-해결)

---

## 1. 소개

**RAG Standard**는 검색 증강 생성(Retrieval-Augmented Generation, RAG) 파이프라인을 표준화하고 효율적으로 관리하기 위한 프로젝트입니다.

문서 로딩부터 벡터 저장, 질의응답 생성까지의 전체 과정을 체계적으로 구성하여 제공합니다.

[AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG)에 영감을 받아 폴더 구조, yaml file 사용을 설계하였습니다.

### 1.1. 프로젝트 목표

* 다양한 RAG 워크플로우를 실험하고 배포할 수 있는 유연하고 확장 가능한 프레임워크 제공

* 데이터 처리, 인덱싱, 검색, 생성 모듈의 표준화 및 재사용성 증대

* RAG 파이프라인의 성능 평가 및 분석 용이성 확보

### 1.2. 핵심 기능

* **문서 처리:** 다양한 문서 형식(HWPX, PDF 등) 지원 및 텍스트 추출, 청킹 기능 (Data Processing 모듈에서 제공 예정)

* **임베딩 생성:** 밀집 벡터(Dense Vector) 및 희소 벡터(Sparse Vector) 생성 지원 (Data Processing 모듈에서 제공 예정)

* **벡터 저장소 연동:** OpenSearch를 활용한 하이브리드 검색 파이프라인 지원

* **LangGraph 기반 워크플로우:** 복잡한 RAG 로직을 유연하게 구성하고 실행

* **LLM 연동:** 설정 가능한 프롬프트 템플릿을 통해 다양한 LLM 모델 활용

* **평가 프레임워크:** 검색 및 생성 성능 평가 기능

* **구성 관리:** YAML 파일을 통한 손쉬운 파이프라인 및 노드 설정

* **로깅 및 오류 처리:** 상세 로깅 및 단계별 오류 처리

---

## 2. 프로젝트 구조

```
RAG-Standard/
├── benchmark/                  # 평가 결과 및 관련 설정 파일 저장
├── configs/                    # 워크플로우 및 주요 설정 YAML 파일
│   ├── main_config.yaml        # 데이터 처리, 인덱싱 통합 설정 (Data Processing용)
│   └── naive_rag_workflow.yaml # Naive RAG 워크플로우 실행 설정
├── data/                       # 원본 데이터 및 QA 데이터셋
│   └── QA/                     # 평가용 QA 데이터셋
├── k8s-stacks/                 # Kubernetes 배포용 YAML 파일
│   └── opensearch/             # OpenSearch 배포 관련 파일
│       ├── Dockerfile
│       └── opensearch_k8s.yaml
├── notebooks/                  # Jupyter 노트북 (예: 실험, 가이드)
│   └── rag_workflow_guide.ipynb # RAG 워크플로우 상세 가이드
├── rag_standard/               # 핵심 RAG 로직 파이썬 패키지
│   ├── __init__.py
│   ├── data_processing/         # 문서 로딩, 청킹, 임베딩 모듈
│   │   └── YW/                  # 데이터 처리 구현
│   │       ├── Loader/          # 문서 로딩 모듈
│   │       │   ├── document_load_final.py
│   │       │   └── load_*.py    # 포맷별 로더
│   │       └── Embedding/       # 임베딩 모듈
│   │           ├── embedding_final.py
│   │           ├── qdrant_final.py
│   │           └── opensearch_final.py
│   ├── graph_workflow/          # LangGraph 기반 워크플로우 정의
│   │   ├── __init__.py
│   │   ├── graph.py            # 그래프 빌더 함수 (예: build_naive_rag_graph)
│   │   ├── node.py            # 그래프 노드 구현 (예: vector_db_search, generate_answer)
│   │   └── state.py            # 그래프 상태 정의 (예: NaiveRAGState)
│   └── utils/                  # 공통 유틸리티 모듈
│       ├── __init__.py
│       ├── config_setting.py   # 설정 파일 로더
│       ├── evaluation_metrics.py # 평가 지표 계산 함수
│       ├── model_call.py       # LLM 및 임베딩 모델 호출
│       ├── opensearch_manager.py # OpenSearch 클라이언트 및 관리
│       ├── setup_logger.py     # 로깅 설정
│       └── sparse_tokenizer.py # 희소 토크나이저 (예: KiwiTokenizer)
├── scripts/                    # 실행 스크립트
│   ├── run_graph_workflow.py   # RAG 워크플로우 실행 (단일 질의)
│   ├── run_evaluation.py       # 평가 스크립트
│   └── cli_chat.py             # 대화형 CLI 인터페이스
├── .env                        # 환경 변수 파일 (API 키, 접속 정보 등)
├── logs/                       # 로그 파일 저장 디렉토리
└── README.md                   # 프로젝트 개요 및 사용법 (본 파일)

```

---

## 3. 설정 및 설치

### 3.1. 사전 준비 사항

* Python 3.12 기준 (`k8s-stacks/jupyter` 참고)

* OpenSearch (실행 중이어야 함)

* LLM 및 임베딩 모델 API 엔드포인트 (실행 중이어야 함)

### 3.2. 저장소 복제

- Clone with SSH
```bash
git clone git@lab.t3q.co.kr:aisvc2024/nlp/rag-standard.git
cd rag-standard
```
- Clone with HTTP
```bash
git clone http://lab.t3q.co.kr:9999/aisvc2024/nlp/rag-standard.git
cd rag-standard
```

### 3.3. 환경 설정

#### 3.3.1. Python 가상 환경
`venv`, `conda`, `uv` 등 원하는 걸로 선택!

#### 3.3.2. 의존성 설치

```bash
pip install -r requirements.txt
```

아마 설치 잘 안될겁니다...   
수동으로 설치하면서 에러날 때마다 추가해주는 게 속편합니다.    
`requirements2.txt`도 시도해보시기 바랍니다!


### 3.4. 환경 변수 (.env)

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 환경에 맞게 채웁니다:

```env
# === 모델 API 정보 ===
# LLM API 엔드포인트 (OpenAI API 형식 호환)
LLM_URL=http://<LLM_API_HOST>:<LLM_API_PORT>/v1
# Text Embedding 모델 API 엔드포인트
TEXT_EMBEDDING_API_URL=http://<EMBEDDING_API_HOST>:<EMBEDDING_API_PORT>/embed

# === OpenSearch 접속 정보 ===
OPENSEARCH_HOST=<YOUR_OPENSEARCH_HOST>
OPENSEARCH_PORT=<YOUR_OPENSEARCH_PORT>
# OPENSEARCH_USER=your_opensearch_user # OpenSearch 인증 사용 시
# OPENSEARCH_PASSWORD=your_opensearch_password # OpenSearch 인증 사용 시

```
`rag_standard/utils/config_setting.py`의 `load_env()` 함수를 통해 로드됩니다.

### 3.5. OpenSearch 설정
* **로컬 또는 기존 OpenSearch 사용 시:** 이미 실행 중인 OpenSearch 인스턴스가 있다면 해당 정보를 `.env` 파일에 설정합니다.
    * 인덱스 매핑에는 텍스트 필드, 밀집 벡터 필드 (`knn_vector`), 희소 토큰 필드 등이 포함되어야 합니다.
    * 하이브리드 검색을 위한 검색 파이프라인 설정은 `rag_standard/indexing/opensearch_search_pipeline.ipynb` 노트북을 참고하여 직접 구성하거나, `scripts/run_graph_workflow.py` 또는 `scripts/cli_chat.py` 실행 시 `naive_rag_workflow.yaml`의 `hybrid_search_config` 설정을 기반으로 자동 생성/업데이트될 수 있습니다.
* **Kubernetes를 사용하여 OpenSearch 신규 구성 시:**
    * 프로젝트 내 `k8s-stacks/opensearch/` 디렉토리의 `opensearch_k8s.yaml` 파일을 참고하여 Kubernetes 환경에 OpenSearch를 배포할 수 있습니다. 이 YAML에는 Nori 분석기가 포함된 OpenSearch 이미지를 사용하는 StatefulSet, Service, PVC 등의 설정이 포함되어 있습니다.
    * 배포 후, 생성된 OpenSearch 서비스의 주소(예: `rag-standard-opensearch-service.default.svc.cluster.local`)와 포트를 `.env` 파일에 설정해야 합니다.

---

## 4. 데이터 처리 (Data Processing)

데이터 처리 모듈은 다양한 소스에서 문서를 로드하고, RAG 파이프라인에 적합한 형태로 가공하는 역할을 담당합니다.

### 4.1. 주요 기능

* **문서 로딩 (Loader)**
  * 다양한 파일 형식 지원: PDF, DOCX, PPT, XLSX, HWP, TXT 등
  * Upstage API를 통한 PDF 처리 지원
  * 페이지 기반 및 토큰 기반 청킹
  * 메타데이터 생성 (파일 정보, 타임스탬프, 토큰 수 등)

* **임베딩 생성 (Embedding)**
  * 밀집 벡터(Dense Vector): BGE 모델 API 사용
  * 희소 벡터(Sparse Vector): BM25 + 한국어 토큰화
  * 한국어 처리: Kiwi 토크나이저 + 사용자 사전 지원
  * 배치 처리 지원

* **벡터 저장소 연동**
  * Qdrant: 밀집/희소 벡터 저장, 코사인 유사도 검색
  * OpenSearch: HNSW 알고리즘, 하이브리드 검색 지원
  * 문서 버전 관리 및 메타데이터 저장

### 4.2. 설정 및 실행

#### 4.2.1. 설정
`configs/main_config.yaml` 파일에서 다음 설정을 관리하여 활용합니다:

```yaml
# --- 메타데이터 값 설정 ---
data_processing_settings:
  version_name: "string"       # 버전 식별자
  root_path: "string"          # 루트 디렉토리 경로
  file_path: "string"          # 입력 파일 디렉토리
  page_tf: "boolean"           # 페이지 기반 청킹 활성화
  token_tf: "boolean"          # 토큰 기반 청킹 활성화
  api_tf: "boolean"            # Upstage API 활성화
  qdrant_tf: "boolean"         # Qdrant 저장소 활성화

# --- Upstage API 설정 ---
upstage_api_settings:
  url: "string"                # Upstage API 엔드포인트
  model: "string"              # Upstage 모델 이름
  max_tokens: number           # 청크당 최대 토큰 수
  overlap_tokens: number       # 청크 간 토큰 중복 수
  token_limit: number          # 최대 토큰 제한

# --- DB 설정 ---
db_settings:
  opensearch_index: "string"   # OpenSearch 인덱스 이름
  qdrant_host: "string"        # Qdrant 호스트
  qdrant_port: "string"        # Qdrant 포트
  qdrant_collection: "string"  # Qdrant 컬렉션 이름
```

#### 4.2.2. 실행
데이터 처리 파이프라인을 실행하려면:

```bash
python scripts/run_data_processing.py
```

실행 시 주의사항:
- `main_config.yaml`의 설정이 올바르게 되어있는지 확인
- 필요한 API 키와 엔드포인트가 `.env` 파일에 설정되어 있는지 확인
- OpenSearch나 Qdrant가 실행 중인지 확인

### 4.3. 출력 구조
사용자가 설정한 내용에 따라 `data` 폴더 내에 아래의 구조로 저장됩니다. (하위 폴더 구조 변동 가능)
* 예를 들어서 API를 사용하지 않고 페이지로 로드하여 Qdrant에 적재했다면,\
아래 구조에서 DOCU_PAGE와 Qdrant 폴더만 생성됨
```
version_name/
├── Interim/           # 중간 결과
├── Split/            # 분할된 문서
│   ├── API_PAGE/    # API 처리된 페이지 청크
│   ├── API_TOKEN/   # API 처리된 토큰 청크
│   ├── DOCU_PAGE/   # 문서 로더 처리된 페이지 청크
│   └── DOCU_TOKEN/  # 문서 로더 처리된 토큰 청크
├── Loader/          # 문서 로더 결과
└── Embedding/       # 최종 임베딩 결과
    ├── Qdrant/     # Qdrant 벡터 저장소
    └── OpenSearch/ # OpenSearch 벡터 저장소
```

### 4.4. 로깅

* 로그 파일 크기 제한: 5MB
* 최대 10개의 백업 로그 파일 유지
* 로그 형식: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
* 각 모듈별 별도 로그 파일 생성

### 4.5. 핵심 구성 요소 상세

#### 4.5.1. 문서 로딩 (Loader)
`rag_standard/data_processing/YW/Loader/` 디렉토리에서 문서 로딩 관련 기능을 제공합니다:
* `document_load_final.py`: 메인 로더 구현
* `load_*.py`: 각 파일 형식별 로더 구현
* `rag_standard/data_processing/YW/Loader/Parsing` 디렉토리 내 파일을 참고하여 페이지/토큰 기반 청킹 지원
* 메타데이터 생성 및 관리

#### 4.5.2. 임베딩 생성 (Embedding)
`rag_standard/data_processing/YW/Embedding/` 디렉토리에서 임베딩 관련 기능을 제공합니다:
* `embedding_final.py`: 메인 임베딩 구현
* `qdrant_final.py`: Qdrant 벡터 저장소 연동
* `opensearch_final.py`: OpenSearch 벡터 저장소 연동
* BGE 모델 API를 통한 밀집 벡터 생성
* BM25 + Kiwi를 통한 희소 벡터 생성

#### 4.5.3. 벡터 저장소 연동
* **Qdrant:**
  * 밀집/희소 벡터 저장
  * 코사인 유사도 기반 검색
  * 문서 버전 관리
  * 메타데이터 저장

* **OpenSearch:**
  * HNSW 알고리즘 기반 검색
  * 하이브리드 검색 지원
  * 한국어 토큰화 지원
  * 문서 버전 관리

### 4.6. 개발 및 사용자 정의

#### 4.6.1. 새로운 문서 로더 추가
1. `rag_standard/data_processing/YW/Loader/` 디렉토리에 새로운 로더 파일 생성
2. 기존 로더와 동일한 인터페이스 구현
3. `document_load_final.py`에 새로운 로더 등록

#### 4.6.2. 새로운 임베딩 모델 추가
1. `rag_standard/data_processing/YW/Embedding/embedding_final.py`에서 코드를 수정해 새로운 임베딩 로직 구현

#### 4.6.3. 새로운 벡터 저장소 추가
1. `rag_standard/data_processing/YW/Embedding/` 디렉토리에 새로운 벡터 저장소 연동 구현
2. 기존 벡터 저장소와 동일한 인터페이스 구현
3. `embedding_final.py`에 새로운 벡터 저장소 등록

---

## 5. RAG 워크플로우 (RAG Workflow)

RAG 워크플로우는 사용자 질의를 입력받아 관련 문서를 검색하고, 이를 바탕으로 LLM이 답변을 생성하는 전체 과정을 LangGraph를 사용하여 그래프 형태로 정의하고 실행합니다.

### 5.1. 워크플로우 설정 (YAML)

RAG 파이프라인의 동작은 주로 `configs/` 디렉토리 내 YAML 파일을 통해 제어됩니다. `naive_rag_workflow.yaml` 파일이 기본적인 RAG 파이프라인 실행을 위한 예제 설정 파일입니다.

#### 5.1.1. 주요 설정 파일: `naive_rag_workflow.yaml`
이 파일은 Naive RAG 워크플로우의 각 구성 요소와 동작 방식을 정의합니다.

#### 5.1.2. `graph_settings`
실행할 LangGraph 모듈 및 그래프 빌더 함수를 지정합니다.
```yaml
graph_settings:
  module: "rag_standard.graph_workflow.graph"  # 그래프 빌더 함수가 있는 파이썬 모듈
  builder_function: "build_naive_rag_graph"   # 호출할 그래프 빌더 함수 이름
  # builder_args: {} # (선택) 빌더 함수에 전달할 인자
```

#### 5.1.3. `tokenizer`
주로 Sparse 검색 시 사용될 토크나이저의 유형과 설정을 정의합니다.
```yaml
tokenizer:
  type: "KiwiTokenizer" # 사용할 토크나이저 클래스 (rag_standard.utils.sparse_tokenizer 참조)
  included_pos_tags:    # KiwiTokenizer 사용 시 추출할 품사 태그 목록
    - NNG # 일반 명사
    - NNP # 고유 명사
    # ... (필요에 따라 추가)
  dictionary_path: ""   # (선택) 사용자 사전 경로 (프로젝트 루트 기준)
```

#### 5.1.4. `graph_node_config`
그래프 내 각 노드(예: `vector_db_search`, `generate_answer`)의 세부 설정을 정의합니다. 이 설정은 그래프 실행 중 `state['config']['graph_node_config']`를 통해 각 노드에서 접근 가능합니다.

* **`vector_db_search` 노드 설정:**
    * `index_name`: OpenSearch 인덱스 이름.
    * `dense_vector_field`: Dense 벡터가 저장된 필드명.
    * `sparse_vector_field`: Sparse 벡터(토큰)가 저장된 필드명.
    * `k`: KNN 검색 시 초기 검색할 문서 수.
    * `size`: 최종적으로 반환할 문서 수.
    * `search_type`: 검색 유형 (`dense`, `sparse`, `hybrid`).
    * `hybrid_search_config` (하이브리드 검색 시):
        * `normalization`: 스코어 정규화 방식 (예: `min_max`).
        * `combination`: 스코어 결합 방식 (예: `arithmetic_mean`).
        * `weights`: Dense와 Sparse 검색 가중치 (예: `[0.3, 0.7]`).

* **`generate_answer` 노드 설정:**
    * `system_prompt_template`: LLM 시스템 프롬프트.
    * `user_prompt_template`: LLM 사용자 프롬프트 템플릿. `{user_query}`와 `{documents}` 변수 사용 가능.
    * `temperature`: LLM 생성 온도.
    * `stream_output`: LLM 답변 스트리밍 여부 (`true` 또는 `false`).
    * 기타 LLM 파라미터 (예: `top_p`, `top_k`, `repetition_penalty`)는 `rag_standard/graph_workflow/node.py`의 `generate_answer` 함수 내 `llm_params`에 직접 추가하거나, YAML에 정의 후 노드에서 읽어 사용하도록 확장할 수 있습니다.

#### 5.1.5. `evaluation_settings`
`scripts/run_evaluation.py` 스크립트 실행 시 사용되는 평가 관련 설정입니다.
* `qa_dataset_path`: QA 데이터셋 Parquet 파일 경로.
* `results_output_dir`: 평가 결과 저장 디렉토리.
* `eval_type`: 평가 유형 (`retrieval`, `generation`, `all`).
* `k_retrieval`: 검색 성능 지표(P@k, R@k, F1@k) 계산 시 사용할 `k`값.

### 5.2. RAG 파이프라인 실행

#### 5.2.1. 단일 질의 실행 (`scripts/run_graph_workflow.py`)
스크립트를 사용하여 단일 사용자 질의에 대한 RAG 워크플로우를 실행합니다.
```bash
python scripts/run_graph_workflow.py configs/naive_rag_workflow.yaml -q "여기에 사용자 질문을 입력하세요"
```
* 첫 번째 인자는 사용할 설정 파일 경로입니다.
* `-q` 또는 `--query` 옵션으로 질문을 직접 전달할 수 있으며, 생략 시 설정 파일 내 `example_query` (존재한다면) 또는 기본 질문이 사용됩니다.

#### 5.2.2. 대화형 CLI 채팅 (`scripts/cli_chat.py`)
`scripts/cli_chat.py`를 통해 대화형으로 RAG 시스템과 상호작용하는 인터페이스를 제공합니다.
```bash
python scripts/cli_chat.py configs/naive_rag_workflow.yaml
```
* 실행 시 설정 파일을 인자로 받습니다.
* 종료하려면 'exit' 또는 'quit'을 입력합니다.

### 5.3. 평가 (`scripts/run_evaluation.py`)
`scripts/run_evaluation.py` 스크립트를 통해 RAG 파이프라인의 검색 및 생성 성능을 평가합니다.
```bash
python scripts/run_evaluation.py configs/naive_rag_workflow.yaml
```
* 평가 설정은 YAML 파일의 `evaluation_settings` 섹션을 따릅니다.

#### 5.3.1. QA 데이터셋 형식
> 반드시 QA 데이터셋을 만들고 `yaml`에 경로 설정해주세요!
>
평가에는 Parquet 형식의 QA 데이터셋이 사용됩니다. (예: `data/QA/qa_dataset.parquet`)
일반적으로 다음 컬럼을 포함합니다:
* `query_id` (str): 각 질문의 고유 ID.
* `query` (str): 사용자 질문.
* `ground_truth_retrieved_doc_ids` (List[str] 또는 Set[str]): 정답 문서 ID 목록 (검색 평가용).
* `ground_truth_answers` (List[str]): 정답 답변 목록 (생성 평가용).

#### 5.3.2. 평가 지표
* **검색 지표 (Retrieval Metrics):**
    * `Precision@k`: 상위 k개 검색 결과 중 정답 문서의 비율.
    * `Recall@k`: 전체 정답 문서 중 상위 k개 검색 결과에 포함된 비율.
    * `F1@k`: Precision@k와 Recall@k의 조화 평균.
* **생성 지표 (Generation Metrics):**
    * `ROUGE-1/2/L (F1-score)`: 생성된 답변과 정답 답변 간의 n-gram 중복 기반 유사도.
    * `BLEU`: 생성된 답변과 정답 답변 간의 n-gram 정밀도 기반 유사도.

#### 5.3.3. 결과 출력
평가 결과는 `evaluation_settings`의 `results_output_dir`에 지정된 디렉토리 (예: `benchmark/`) 하위에 각 실행별 고유 시도 번호(0, 1, 2...)로 생성된 폴더 내에 저장됩니다.
* `detailed_evaluation_results.csv`: 각 질의별 상세 평가 지표.
* `summary_metrics.csv`: 전체 평균 평가 지표.
* 사용한 설정 파일(`*.yaml`)의 복사본도 함께 저장되어 실험 재현성을 높입니다.

### 5.4. 핵심 구성 요소 상세
> 여기부터는 `notebooks/rag_workflow_guide.ipynb`와 함께 보시는 것을 추천드립니다!

#### 5.4.1. 그래프 워크플로우 (LangGraph)
복잡한 RAG 로직은 LangGraph를 사용하여 상태 기반 그래프로 표현됩니다.   
각 노드는 특정 작업을 수행하고, 상태를 업데이트하여 다음 노드로 전달합니다.

#### 5.4.2. 상태 (State)
그래프 실행 중 노드 간에 전달되는 핵심 데이터 구조입니다. `NaiveRAGState` (`rag_standard/graph_workflow/state.py`에 정의)는 `naive_rag_workflow`의 주요 상태를 정의하며 다음 필드를 포함할 수 있습니다:
* `config` (Dict): 전체 워크플로우 설정 (`*.yaml` 파일 내용).
* `user_query` (str): 사용자의 원본 질문.
* `sparse_tokenizer` (Any): Sparse 검색에 사용될 토크나이저 인스턴스 (예: `KiwiTokenizer`).
* `opensearch_manager` (Any): OpenSearch와의 상호작용을 관리하는 `OpenSearchManager` 인스턴스.
* `retrieved_documents` (List[dict]): `vector_db_search` 노드에서 검색된 문서 목록.
* `llm_answer` (str): `generate_answer` 노드에서 생성된 최종 LLM 답변.
* `llm_stream_handled_by_node` (Optional[bool]): LLM 답변이 노드 레벨에서 스트리밍으로 처리되었는지 여부.

#### 5.4.3. 노드 (Node)
그래프의 각 단계를 나타내는 함수 또는 실행 가능한 객체입니다. `rag_standard/graph_workflow/node.py`에 주요 노드들이 정의되어 있습니다.
* **`vector_db_search`**: 사용자 질의(`user_query`)와 설정(`config`)을 기반으로 `opensearch_manager`를 사용하여 OpenSearch에서 관련 문서를 검색하고 `retrieved_documents`를 업데이트합니다. 검색 유형(dense, sparse, hybrid)은 YAML 설정을 따릅니다.
* **`generate_answer`**: 검색된 문서(`retrieved_documents`)와 사용자 질의(`user_query`)를 사용하여 프롬프트를 구성하고, LLM을 호출하여 답변을 생성합니다. 생성된 답변은 `llm_answer`에 저장되며, 스트리밍 설정에 따라 출력을 직접 처리할 수 있습니다 (`llm_stream_handled_by_node` 플래그 업데이트).

#### 5.4.4. 그래프 빌드
`rag_standard.graph_workflow.graph` 모듈 내 `build_naive_rag_graph`와 같은 함수에서 노드와 엣지(흐름)를 정의하여 실행 가능한 그래프를 구성합니다.

### 5.5. 토큰화
주로 한국어 처리를 위해 `kiwipiepy` 기반의 `KiwiTokenizer` (`rag_standard/utils/sparse_tokenizer.py`에 정의)가 사용됩니다.
* `configs/*.yaml` 파일의 `tokenizer` 섹션에서 품사 태그, 사용자 사전 등을 설정하여 특정 도메인에 맞게 최적화할 수 있습니다.
* Sparse 벡터 생성을 위한 키워드 추출 등에 활용됩니다.

### 5.6. OpenSearch 연동
* `rag_standard.utils.opensearch_manager.OpenSearchManager` 클래스를 통해 OpenSearch 클라이언트 연결 및 관리가 이루어집니다.
* 문서 청크, 밀집 임베딩, 희소 토큰 등을 저장하고 검색합니다.
* 하이브리드 검색을 위한 검색 파이프라인(예: `hybrid_pipeline_example`)은 `scripts/run_graph_workflow.py` 등에서 YAML 설정에 따라 동적으로 생성/관리될 수 있습니다.

### 5.7. LLM 연동
* `.env` 파일에 정의된 `LLM_URL`을 통해 외부 LLM API를 호출합니다.
* `configs/*.yaml` 파일의 `generate_answer` 노드 설정에서 시스템 프롬프트, 사용자 프롬프트 템플릿, `temperature` 등의 파라미터를 조정할 수 있습니다.
* 스트리밍 출력을 지원하며, `generate_answer` 노드에서 직접 처리하거나 (`llm_stream_handled_by_node=True`), 파이프라인 실행기(예: `cli_chat.py`)에서 처리할 수 있습니다.

### 5.8. 개발 및 사용자 정의

#### 5.8.1. 새로운 그래프 노드 추가
1.  `rag_standard/graph_workflow/node.py` (또는 신규 파이썬 파일)에 새로운 노드 함수를 작성합니다.
2.  새로운 노드는 해당 그래프의 상태 (예: `NaiveRAGState`)를 입력받고, 업데이트된 상태를 반환하도록 설계합니다.
3.  필요한 설정은 `configs/*.yaml` 파일의 `graph_node_config`에 추가하고, 노드 함수 내에서 `state['config']`를 통해 접근합니다.

#### 5.8.2. 사용자 정의 그래프 빌더 생성
1.  `rag_standard/graph_workflow/graph.py`에 새로운 그래프 빌더 함수를 작성합니다.
2.  새로운 노드들을 포함하여 그래프의 흐름(엣지)을 정의합니다.
3.  `configs/*.yaml` 파일의 `graph_settings`에서 새로운 빌더 함수 모듈과 이름을 지정합니다.

#### 5.8.3. 토크나이저 수정
* 다른 한국어 토크나이저 또는 다국어 토크나이저를 사용하려면, `rag_standard/utils/sparse_tokenizer.py`에 해당 토크나이저의 래퍼 클래스(기존 `SparseTokenizer` 추상 클래스 상속)를 추가하고, `configs/*.yaml` 파일의 `tokenizer.type`에서 선택할 수 있도록 수정합니다.

---

## 6. 문제 해결
* **로그 확인:** `logs/` 디렉토리의 로그 파일(예: `opensearch_manager.log`, `run_graph_workflow.log` 등)을 통해 오류의 원인을 파악합니다. 각 스크립트나 모듈은 자체 로그 파일을 생성할 수 있습니다.
* **환경 변수:** `.env` 파일의 API URL, 호스트, 포트, 인증 정보 등이 올바르게 설정되었는지 확인합니다.
* **OpenSearch 연결:** OpenSearch 서버가 정상적으로 실행 중이고, 네트워크 연결에 문제가 없는지 확인합니다. (`k8s-stacks/opensearch/check_connection.ipynb` 참고) 인덱스 및 검색 파이프라인 설정을 확인합니다.
* **의존성:** `requirements.txt`에 명시된 모든 Python 라이브러리가 올바르게 설치되었는지 확인합니다.
* **설정 파일 경로:** 스크립트 실행 시 YAML 설정 파일 경로가 정확한지 확인합니다.
