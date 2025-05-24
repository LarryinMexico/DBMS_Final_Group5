FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
COPY app ./app

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y gcc build-essential

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]