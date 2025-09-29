FROM jupyter/pyspark-notebook:spark-3.1.2

USER root

# 필수 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        build-essential \
        cmake \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# 앱 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스 복사
COPY . .

# FastAPI 앱 실행
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8001"]
