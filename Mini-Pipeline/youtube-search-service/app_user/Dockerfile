# FastAPI Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

# Copy application code
COPY . .

# Run FastAPI server
CMD ["uvicorn", "main:app", "--proxy-headers", "--reload", "--host", "0.0.0.0", "--port", "8002"]
