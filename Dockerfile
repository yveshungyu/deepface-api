# 使用一個包含 Python 的基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝 OpenCV 需要的系統級依賴
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴列表檔案
COPY requirements.txt .

# 安裝 Python 函式庫
RUN pip install --no-cache-dir -r requirements.txt

# 複製您的應用程式程式碼
COPY . .

# 設定環境變數，讓 Flask 知道要執行哪個檔案
ENV FLASK_APP=app.py

# 使用 Gunicorn 啟動應用程式的指令
# 監聽 Render 指定的 PORT，並設定 4 個 worker
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 4 --limit-request-line 8192 --limit-request-field-size 16384 --timeout 60 app:app