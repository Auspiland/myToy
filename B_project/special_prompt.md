# 프로젝트: AI 

## 개요

내부 **데이터 파이프라인/API** – FastAPI 기반의 비동기 API, PostgreSQL(영구 저장), Redis(캐시/작업큐)

## 빠른 시작

### 개발 환경 실행

```bash
# Docker Compose로 전체 서비스 시작 (로컬 개발)
docker-compose -f docker-compose.dev.yml up -d

# 접속
# Backend API: http://localhost:8000
# API 문서: http://localhost:8000/docs
```

📖 **자세한 내용**: [배포 및 환경 관리 가이드](./DEPLOY.md)

## 기술 스택

### Backend

* **프레임워크**: Python 3.11+ + FastAPI
* **비동기**: async/await (asyncio)
* **ORM**: SQLAlchemy 2.0 (async)
* **검증**: Pydantic v2
* **API 문서**: OpenAPI (Swagger) 자동 생성
* **패키지 관리**: uv (초고속 Python 패키지 관리자)
* **코드 품질**: ruff (linting + formatting 통합)

### 파이프라인 인프라

* **데이터베이스**: PostgreSQL (asyncpg)
* **캐시/작업 큐**: Redis

## 프로젝트 구조

```
portal/
├── backend/              # 백엔드 API 서버 (파이프라인 제어/엔드포인트)
│   ├── app/
│   │   ├── api/         # API 엔드포인트 (라우터)
│   │   ├── core/        # 설정, 보안, 의존성
│   │   ├── models/      # SQLAlchemy 모델
│   │   ├── schemas/     # Pydantic 스키마(데이터 계약)
│   │   ├── services/    # 비즈니스 로직(ETL/검증/트랜잭션 경계)
│   │   └── main.py      # FastAPI 앱 진입점
│   ├── tests/           # 테스트 코드
│   ├── Dockerfile       # Backend Docker 이미지
│   ├── .env.example     # 환경 변수 예시
│   ├── pyproject.toml   # 프로젝트 설정 (uv + ruff)
│   └── uv.lock          # 의존성 잠금 파일
│
├── .gitlab-ci.yml       # GitLab CI/CD 파이프라인
├── docker-compose.yml   # 로컬 개발/테스트용 Docker Compose (Backend + DB + Redis)
├── docker-compose.prod.yml  # 프로덕션 시뮬레이션용
│
└── docs/                # 프로젝트 문서
    ├── CHANGELOG.md
    ├── README.md
    ├── decisions/
    ├── features/
    └── refactoring/
```

## 개발 가이드라인

### ⚠️ 핵심 원칙: 유지보수성 최우선

이 프로젝트는 지속적인 유지보수와 빠른 대응이 필수입니다.

* **재사용성**: 모든 모듈/서비스는 재사용 가능하도록 설계
* **리팩토링 친화적**: 변경에 유연한 구조 유지
* **빠른 응대**: 명확한 구조로 빠른 수정 가능하도록 설계

## 코딩 표준

### 📌 공통 표준 (Backend 중심)

#### 기본 원칙

* **DRY 원칙**: 중복 코드 절대 금지, 공통 로직은 즉시 추출
* **명확한 네이밍**: 함수/변수명으로 기능 파악 가능하도록
* **단일 책임**: 하나의 함수/클래스는 하나의 책임만
* **작은 파일 유지**: 한 파일은 200줄 이하 권장
* **명확한 의존성**: 순환 참조 절대 금지

#### 네이밍 컨벤션

* **함수/메서드**: 동사로 시작 (`get_user_data`, `validate_email`)
* **변수/속성**: 명사 (`user_name`, `total_count`)
* **상수**: 대문자 스네이크케이스 (`MAX_RETRY_COUNT`)
* **Boolean**: is/has/can 접두사 (`is_valid`, `has_permission`)

#### 에러 처리

* 예상 가능한 에러는 명시적으로 처리
* 에러 메시지는 사용자/운영자 친화적으로 작성
* 로깅 레벨 적절히 사용 (DEBUG, INFO, WARNING, ERROR)

---

### 🐍 Backend 표준 (Python + FastAPI)

#### Python 규칙

* **PEP 8** 준수 (ruff로 자동 검사 및 포맷팅)
* Type Hints 필수 사용 (`def func(x: int) -> str:`)
* Docstring 작성 (Google Style)
* f-string 사용 (문자열 포매팅)
* **ruff**: linting + formatting 통합 도구

#### FastAPI 규칙

* **비동기 우선**: DB 조회, 외부 I/O는 `async def`
* **의존성 주입**: `Depends()`로 공통 로직 재사용
* **Pydantic 스키마**: 요청/응답 검증 및 문서화(데이터 계약)
* **라우터 분리**: 도메인별 라우터 파일 분리 (`api/users.py`, `api/chat.py`)
* **상태 코드 명시**: 각 엔드포인트에 적절한 HTTP 상태 코드 지정

#### 데이터베이스 (asyncpg + SQLAlchemy 2.0)

* **asyncpg 필수**: PostgreSQL 비동기 드라이버
* **연결 URL 형식**: `postgresql+asyncpg://user:pass@host:port/db`
* **SQLAlchemy 비동기 API**: `AsyncSession`, `async with` 패턴
* **커넥션 풀 관리**: `create_async_engine`으로 풀 설정
* **트랜잭션 관리**: 명시적 트랜잭션 (`async with session.begin()`)

##### 데이터베이스 설정 예시

```python
# core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/portal"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 개발 환경에서만
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

##### 모델 정의 예시

```python
# models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

##### 서비스 레이어에서 사용 예시

```python
# services/user_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate, UserResponse

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
```

##### 라우터에서 사용 예시

```python
# api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.user_service import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    user = await service.create_user(user_data)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user
```

#### 프로젝트 구조 원칙

```python
# ✅ 좋은 예
app/
├── api/
│   ├── deps.py          # 공통 의존성
│   ├── users.py         # 사용자 관련 엔드포인트
│   └── chat.py          # 채팅/잡 트리거 등 엔드포인트
├── core/
│   ├── config.py        # 환경 설정
│   └── security.py      # 인증/보안
├── models/
│   └── user.py          # SQLAlchemy 모델
├── schemas/
│   └── user.py          # Pydantic 스키마
└── services/
    └── user_service.py  # 비즈니스 로직
```

#### 네이밍

* 파일/모듈: snake_case (`user_service.py`, `api_client.py`)
* 클래스: PascalCase (`UserService`, `ChatMessage`)
* 함수/변수: snake_case (`get_user_by_id`, `total_count`)
* 상수: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)

#### 비즈니스 로직 분리

* ❌ **나쁜 예**: 라우터에 비즈니스 로직 직접 작성

```python
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    # DB 조회, 검증, 변환 로직 모두 여기에...
    pass
```

* ✅ **좋은 예**: 서비스 레이어로 분리

```python
# api/users.py
@router.get("/users/{user_id}")
async def get_user(user_id: int, service: UserService = Depends()):
    return await service.get_user(user_id)
```

#### 에러 처리

```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="사용자를 찾을 수 없습니다"
)
```

### 리팩토링 가이드

* **지속적 개선**: 코드 작성 시 항상 개선 가능성 고려
* **안전한 리팩토링**: 타입 시스템 활용으로 안전성 확보
* **즉시 리팩토링**: 중복 발견 시 즉시 공통화
* **테스트 우선**: 리팩토링 전 동작 검증 방법 확보

### 유지보수성 체크리스트

✅ 다른 흐름에서 재사용 가능한가?
✅ 6개월 후 다른 개발자가 이해할 수 있는가?
✅ 인터페이스 변경 시 영향 최소화되는가?
✅ 비즈니스 로직과 I/O가 명확히 분리되어 있는가?
✅ 중복된 코드가 없는가?

## 명령어 (Backend)

```bash
cd backend

# 개발 서버 실행 (hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 의존성 설치 (uv 사용 - 초고속)
uv pip install -r pyproject.toml
# 또는 uv sync (권장)
uv sync

# 패키지 추가
uv add fastapi uvicorn sqlalchemy asyncpg

# 개발 의존성 추가
uv add --dev pytest ruff mypy

# 테스트 실행
pytest
# 또는 uv로 실행
uv run pytest

# 코드 검사 및 포맷팅 (ruff - 올인원)
ruff check .          # linting 검사
ruff check --fix .    # 자동 수정
ruff format .         # 코드 포맷팅 (black 스타일)

# 타입 체크
mypy app/

# 데이터베이스 마이그레이션
alembic upgrade head
alembic current
alembic history
alembic downgrade -1

# 초기 데이터 생성 (예: 공지/메타데이터 시드)
python seed_notifications.py
```

## 개발 프로세스 및 배포 전략

### 🔄 개발 워크플로우

```
로컬 개발 (Windows)
    ↓
Docker 로컬 테스트
    ↓
GitLab Push
    ↓
GitLab CI/CD 파이프라인
```

### 💻 환경별 구성

#### 1. 로컬 개발 환경 (Windows)

```bash
# Backend 로컬 실행
cd backend
uv sync
uvicorn app.main:app --reload
```

**환경 변수**: `.env.local` (git 무시)

#### 2. Docker 로컬 테스트 (Windows)

```bash
# Backend + DB + Redis
docker-compose up -d

# 빌드 후 실행
docker-compose up --build

# 로그 확인
docker-compose logs -f

# 종료
docker-compose down
```

**환경 변수**: `.env.docker` (git 무시)

### 🔐 환경 변수 관리 전략

#### 환경 분리

* **로컬 개발**: `.env.local`
* **Docker 테스트**: `.env.docker`
* **운영 환경**: GitLab CI Variables (시스템 환경 변수)

#### Backend 환경 변수 예시 (`.env.example`)

```bash
# 애플리케이션 설정
APP_NAME=AI Assistant Portal
APP_ENV=development  # development, staging, production
DEBUG=true

# 데이터베이스 (asyncpg 필수)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_portal

# API 설정
API_V1_PREFIX=/api/v1

# 보안 (프로덕션에서 필수 변경, config.py에서 검증)
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS (쉼표로 구분)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 캐시/큐
REDIS_URL=redis://redis:6379/0

# 데모 자격증명 (개발 환경 전용)
DEMO_EMAIL=demo@example.com
DEMO_PASSWORD=password123!
```

**중요 사항**:

* `APP_ENV=production`에서 SECRET_KEY 검증(기본값 금지)
* SECRET_KEY 생성: `openssl rand -hex 32`

#### 환경 변수 우선순위 (Pydantic Settings 로드 순서)

1. **시스템 환경 변수** (최우선)
2. **`.env` 파일** (`.env.local`, `.env.docker` 등)
3. **기본값** (config.py)

#### ⚠️ 보안 규칙

* **절대 커밋 금지**: `.env.local`, `.env.docker`, `.env.production`
* **Git 커밋 허용**: `.env.example` (템플릿만)
* **Secret 관리**: GitLab CI Variables
* **키 로테이션**: SECRET_KEY/JWT_SECRET 주기적 변경

### 🐳 Docker 구성

#### docker-compose.yml (Backend + DB + Redis)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/portal
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app  # hot reload

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: portal
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 🚀 GitLab CI/CD 파이프라인

#### .gitlab-ci.yml 주요 스테이지

```yaml
stages:
  - test          # 코드 품질 검사, 단위 테스트
  - build         # Docker 이미지 빌드
  - deploy-dev    # Dev 환경 배포
  - deploy-staging # Staging 환경 배포 (수동)
  - deploy-prod   # Prod 환경 배포 (수동, 승인 필요)
```

#### CI/CD 플로우

1. **test**: ruff, mypy, pytest 실행
2. **build**: Docker 이미지 빌드 및 레지스트리 푸시
3. **deploy**: 환경별 배포 (GitLab CI Variables 활용)

### ✅ 배포 체크리스트

#### 로컬 개발 후

* [ ] 로컬에서 Backend + DB/Redis 정상 동작 확인
* [ ] `docker-compose up`으로 Docker 환경 테스트
* [ ] `.env.example` 업데이트 (새 변수 추가 시)
* [ ] ruff, mypy, pytest 통과 확인

#### GitLab Push 전

* [ ] 민감한 정보 제거 확인 (API 키, 비밀번호)
* [ ] `.gitignore`에 `.env.*` 포함 확인
* [ ] 커밋 메시지 명확히 작성

#### 운영 배포 전

* [ ] 테스트 환경에서 충분한 검증
* [ ] DB 마이그레이션 스크립트 준비
* [ ] 롤백 계획 수립

## 주요 참고사항

* **데이터 품질/신뢰성 최우선** – 스키마(contracts) 준수, 유효성 검증, 트랜잭션 일관성
* **비동기 작업 운영성** – 재시도/백오프, 아이들포턴시(idempotency), 타임아웃/서킷브레이커 고려
* **관측 가능성** – 구조적 로깅, 메트릭, 트레이싱
* **환경 변수는 절대 커밋하지 않기** – `.env.example`만 커밋

## Claude Code 작업 시 주의사항

### 코드 작성 시

* **재사용성 우선**: 기존 서비스/유틸 재사용 우선
* **즉시 리팩토링**: 중복 발견 시 공통화
* **타입 안정성**: 모든 함수/반환에 명시적 타입
* **작은 단위**: 작은 서비스/함수로 조합
* **Backend 코드 작성 후**: `ruff check --fix .`로 코드 품질 확인

### 리팩토링 시

* **영향 범위 파악**: 사용처 서치
* **타입 시스템 활용**: 타입 에러로 영향 추적
* **점진적 개선**: 단계별 변경
* **기존 패턴 준수**: 프로젝트 코드 스타일 유지

### 빠른 응대를 위한 원칙

* **명확한 구조**: 폴더/파일만 보고도 위치 파악 가능
* **일관된 패턴**: 같은 기능은 같은 방식
* **충분한 타입**: 타입 정의로 이해 시간 단축
* **의미있는 네이밍**: 주석 없이 의도 파악 가능

### Backend 개발 시 필수 체크

* ✅ Type Hints 모든 함수에 추가했는가?
* ✅ 비동기 함수 (`async def`) 적절히 사용했는가?
* ✅ 데이터베이스 연결은 asyncpg를 사용하는가? (`postgresql+asyncpg://`)
* ✅ SQLAlchemy 비동기 API (`AsyncSession`, `async with`)를 사용했는가?
* ✅ 비즈니스 로직을 서비스 레이어로 분리했는가?
* ✅ `ruff check --fix .` 실행했는가?
* ✅ Pydantic 스키마로 요청/응답 검증했는가?
* ✅ 환경 변수를 하드코딩하지 않고 `config.py`에서 관리하는가?
* ✅ 새로운 환경 변수 추가 시 `.env.example` 업데이트했는가?
* ✅ 민감한 정보(SECRET_KEY 등)를 코드에 포함하지 않았는가?

## 문서화 원칙

### 진행 사항 문서화 필수

모든 작업 내용은 반드시 문서로 남겨야 합니다.

### 문서 저장 위치

```
portal/
└── docs/
    ├── CHANGELOG.md
    ├── README.md
    ├── decisions/
    ├── features/
    └── refactoring/
```

### 문서 작성 규칙

#### CHANGELOG.md (필수)

```markdown
# 변경 이력

## [2024-10-30] 파이프라인 구조 개선
### 변경 내용
- ETL 서비스 공통화
- 중복 변환 로직 제거

### 영향 범위
- `services/etl_service.py` 신규 생성
- `api/ingest.py` 수정

### 관련 문서
- [features/etl-service.md](features/etl-service.md)
```

#### docs/README.md (목차)

```markdown
# 프로젝트 문서 목차

## 최근 변경사항
- [2024-10-30] 파이프라인 구조 개선
- [2024-10-29] 초기 프로젝트 설정

## 기능별 문서
- [인증/권한](features/authentication.md)
- [데이터 수집/검증/적재](features/ingestion.md)

## 리팩토링 이력
- [공통 변환 로직 추출](refactoring/transform-extraction.md)
```

### 문서 작성 시 포함 사항

1. **작업 날짜**: YYYY-MM-DD
2. **작업 요약**: 한 줄 요약
3. **변경 내용**: 구체적인 변경 사항
4. **영향 범위**: 수정된 파일 목록
5. **이유**: 변경 이유
6. **다음 단계**: 추가 작업 필요 사항 (선택)

### Claude Code 문서화 가이드

* 작업 완료 후 **반드시** CHANGELOG.md 업데이트
* 주요 기능 추가 시 features/ 에 상세 문서 작성
* 리팩토링 시 refactoring/ 에 변경 이력 기록
* docs/README.md 목차 최신 상태 유지

