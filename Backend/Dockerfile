# 使用輕量版 Python image
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製專案進 image
COPY . .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 對外開放 port 8000
EXPOSE 8000

# 啟動 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
