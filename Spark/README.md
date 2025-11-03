# Road Infrastructure Risk Assessment Pipeline

고속도로 및 도로 인프라의 위험도를 평가하는 **Bronze/Silver/Gold** 아키텍처 기반 Spark + Airflow 파이프라인입니다.

## 개요

이 파이프라인은 도로 시설물(교량, 터널 등)의 다양한 속성을 분석하여 구조적 위험도를 평가합니다.

### 주요 기능

- **Bronze Layer**: CSV 원시 데이터 수집 및 스키마 검증
- **Silver Layer**: 룩업 테이블 조인, 파생 변수 생성
- **Gold Layer**: 위험도 점수 계산, 집계 리포트 생성
- **Data Quality**: 각 레이어별 데이터 품질 검증
- **Monitoring**: 구조화된 로깅 및 메트릭 수집

## 디렉터리 구조

```
Spark/
├── dags/
│   └── road_risk_pipeline.py          # Airflow DAG
├── conf/
│   ├── pipeline.conf.yaml              # 파이프라인 설정
│   └── load_grade_lookup.csv           # 설계하중 룩업 테이블
├── data/
│   └── roads.csv                       # 샘플 데이터
├── spark_jobs/
│   ├── common/                         # 공통 유틸리티
│   │   ├── __init__.py
│   │   ├── config_loader.py            # 설정 로더
│   │   ├── spark_factory.py            # Spark 세션 팩토리
│   │   ├── logger.py                   # 로깅 유틸리티
│   │   └── data_quality.py             # 데이터 품질 검증
│   ├── 01_ingest_csv.py                # Bronze: 데이터 수집
│   ├── 02_enrich_lookup.py             # Silver: 데이터 보강
│   ├── 03_compute_scores.py            # Gold: 점수 계산
│   ├── 04_compute_risk.py              # Gold: 위험도 계산
│   └── 05_publish_aggregates.py        # Gold: 집계 리포트
├── output/                             # 출력 디렉터리
│   ├── bronze/
│   ├── silver/
│   └── gold/
└── logs/                               # 로그 디렉터리
```

## 위험도 평가 방법론

### 성분 점수 (Component Scores)

각 시설물에 대해 6가지 위험 성분 점수를 계산합니다 (0-1 스케일):

1. **S_용량 (Capacity)**: 설계하중 대비 요구하중 부족도
   - `max(0, 1 - 설계하중/요구하중)`

2. **S_노후 (Age)**: 시설물 경과연수 (50년 기준 정규화)
   - `min(1.0, 경과연수/50)`

3. **S_교통 (Traffic)**: 교통량 (40,000대/일 기준 정규화)
   - `min(1.0, 교통량/40000)`

4. **S_경간 (Span)**: 최대 경간장 (80m 기준 정규화)
   - `min(1.0, 최대경간장/80)`

5. **S_폭 (Width)**: 유효폭 대비 총폭 활용도
   - `max(0, 1 - 유효폭/총폭)`

6. **S_메타 (Metadata)**: 메타데이터 완성도
   - 상부구조/하부구조 누락 시 0.3

### 종합 위험도 (Overall Risk)

가중 평균으로 계산:

```
RISK = 0.35×S_용량 + 0.25×S_노후 + 0.20×S_교통
     + 0.10×S_경간 + 0.05×S_폭 + 0.05×S_메타
```

### 위험 등급

- **높음**: RISK ≥ 0.6
- **보통**: 0.3 ≤ RISK < 0.6
- **낮음**: RISK < 0.3

## 설치 및 실행

### 사전 요구사항

- Python 3.8+
- Apache Spark 3.x
- Apache Airflow 2.x
- PyYAML

### 설치

```bash
# Python 패키지 설치
pip install pyspark apache-airflow pyyaml

# 또는 requirements.txt 사용 (있다면)
pip install -r requirements.txt
```

### 로컬 실행 (테스트)

개별 Spark 작업을 로컬에서 실행:

```bash
# 환경 변수 설정
export BASE_PATH="C:/Users/T3Q/jeonghan/DUMMY/Spark"
export BRONZE_PATH="$BASE_PATH/output/bronze"
export SILVER_PATH="$BASE_PATH/output/silver"
export GOLD_PATH="$BASE_PATH/output/gold"
export INPUT_CSV="$BASE_PATH/data/roads.csv"
export LOOKUP_LOAD_GRADE_CSV="$BASE_PATH/conf/load_grade_lookup.csv"
export PARTITION_DT="20251103"

# Bronze layer 실행
cd spark_jobs
python 01_ingest_csv.py

# Silver layer 실행
python 02_enrich_lookup.py

# Gold layer 실행
python 03_compute_scores.py
python 04_compute_risk.py
python 05_publish_aggregates.py
```

### Airflow 실행

```bash
# Airflow 홈 설정
export AIRFLOW_HOME=~/airflow

# DAG 디렉터리 설정 (airflow.cfg)
# dags_folder = /path/to/Spark/dags

# Airflow 초기화
airflow db init

# Webserver 시작
airflow webserver -p 8080

# Scheduler 시작 (별도 터미널)
airflow scheduler

# 웹 브라우저에서 접속
# http://localhost:8080
```

## 설정

### 환경 변수

주요 환경 변수:

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `BASE_PATH` | 프로젝트 루트 경로 | `/opt/road` |
| `BRONZE_PATH` | Bronze 출력 경로 | `{BASE_PATH}/output/bronze` |
| `SILVER_PATH` | Silver 출력 경로 | `{BASE_PATH}/output/silver` |
| `GOLD_PATH` | Gold 출력 경로 | `{BASE_PATH}/output/gold` |
| `INPUT_CSV` | 입력 CSV 경로 | `{BASE_PATH}/data/roads.csv` |
| `LOOKUP_LOAD_GRADE_CSV` | 룩업 테이블 경로 | `{BASE_PATH}/conf/load_grade_lookup.csv` |
| `PARTITION_DT` | 파티션 날짜 (YYYYMMDD) | `20251103` |

### 설정 파일

`conf/pipeline.conf.yaml` 파일에서 파이프라인 파라미터를 설정할 수 있습니다:

```yaml
risk_weights:
  capacity: 0.35
  age: 0.25
  traffic: 0.20
  span: 0.10
  width: 0.05
  metadata: 0.05
```

## 출력 데이터

### Bronze Layer

- **경로**: `output/bronze/dt={YYYYMMDD}/`
- **형식**: Parquet (Snappy 압축)
- **내용**: 원시 CSV 데이터 + 기본 정제

### Silver Layer

- **경로**: `output/silver/dt={YYYYMMDD}/`
- **형식**: Parquet (Snappy 압축)
- **내용**: 룩업 조인, 파생 변수 추가
  - `설계하중_ton`: 설계하중 톤 단위
  - `요구하중_ton`: 도로 종류별 요구하중
  - `경과연수`: 2025 - 준공년도
  - `용량비율`: 설계하중/요구하중

### Gold Layer

#### 1. Scores (`gold/scores/dt={YYYYMMDD}/`)
- Silver 데이터 + 6가지 성분 점수
- 컬럼: `S_용량`, `S_노후`, `S_교통`, `S_경간`, `S_폭`, `S_메타`

#### 2. Risk (`gold/risk/dt={YYYYMMDD}/`)
- Scores + 종합 위험도 및 등급
- 컬럼: `RISK`, `RISK_LEVEL`

#### 3. Aggregates

- **지역별 집계** (`gold/agg_by_region/dt={YYYYMMDD}/`):
  - 컬럼: `시도`, `시군구`, `RISK_LEVEL`, `시설수`

- **노선별 집계** (`gold/agg_by_route/dt={YYYYMMDD}/`):
  - 컬럼: `노선명`, `avg_risk`, `시설수`, `높음`, `보통`, `낮음`

- **연령대별 집계** (`gold/agg_by_age_group/dt={YYYYMMDD}/`):
  - 컬럼: `age_group`, `시설수`, `avg_risk`, `높음`, `보통`, `낮음`

- **고위험 시설 리포트** (`gold/report_high_risk/dt={YYYYMMDD}/`):
  - 위험도 '높음' 시설만 필터링

- **요약 통계** (`gold/summary_stats/dt={YYYYMMDD}/`):
  - 전체 파이프라인 요약 통계

## 데이터 품질 검증

각 레이어에서 다음과 같은 검증을 수행합니다:

### Bronze Layer
- 데이터프레임이 비어있지 않은지 확인
- 필수 컬럼 존재 여부
- NULL 비율 체크
- 준공년도 범위 검증 (1900-2025)

### Silver Layer
- 룩업 조인 성공률 (설계하중, 요구하중)
- 파생 변수 계산 성공률
- 경과연수 범위 검증

### Gold Layer
- 점수 범위 검증 (0-1)
- NULL 값 존재 여부
- 위험도 분포 검증
- 위험 등급 유효성

## 개선 사항

원본 설계 대비 개선된 내용:

### 1. 공통 모듈화
- `common/` 패키지로 재사용 가능한 유틸리티 분리
- ConfigLoader, SparkFactory, Logger 등

### 2. 에러 처리
- 모든 작업에 try-except-finally 추가
- 구조화된 로깅
- 명확한 exit code 반환

### 3. 데이터 품질 검증
- DataQualityValidator 프레임워크
- 각 레이어별 검증 규칙
- 검증 결과 로깅

### 4. 메트릭 수집
- MetricsLogger로 처리 통계 수집
- NULL 통계, 처리 속도 등
- 위험도 분포 통계

### 5. 설정 관리
- YAML 설정 파일 지원
- 환경 변수 오버라이드
- 계층적 설정 우선순위

### 6. 확장성
- Task Group으로 DAG 구조화
- 파라미터화된 Spark 설정
- 쉬운 Kubernetes 전환 가능

## 트러블슈팅

### 1. Spark 메모리 부족
```bash
# executor/driver 메모리 증가
export SPARK_DRIVER_MEMORY=4g
export SPARK_EXECUTOR_MEMORY=4g
```

### 2. 파일 경로 오류
- 절대 경로 사용 권장
- Windows에서는 `/` 또는 `\\` 사용

### 3. 룩업 테이블 조인 실패
- `conf/load_grade_lookup.csv` 파일 확인
- 공백 처리 규칙 확인 (자동 정규화됨)

## 향후 개선 계획

- [ ] Delta Lake 통합
- [ ] 실시간 스트리밍 지원
- [ ] ML 기반 위험도 예측 모델
- [ ] Kubernetes SparkOperator 지원
- [ ] Great Expectations 통합
- [ ] 대시보드 (Grafana/Superset)

## 라이선스

MIT License

## 문의

이슈나 개선 제안은 프로젝트 저장소에 등록해주세요.
