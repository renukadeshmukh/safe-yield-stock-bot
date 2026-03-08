FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest pytest-asyncio

COPY src/ src/
COPY tests/ tests/
COPY run_telegram.py pyproject.toml ./

CMD ["python", "run_telegram.py"]
