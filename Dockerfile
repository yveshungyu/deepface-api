# 使用一個穩定的 Python 版本
FROM python:3.9-slim

# 設定環境變數，防止 Python 將日誌緩存
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /app

# 安裝 OpenCV 需要的系統級依賴
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 複製並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式程式碼
COPY . .

# 【最終修正】使用 shell 格式啟動 Gunicorn，確保 ${PORT} 變數被正確解析
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app