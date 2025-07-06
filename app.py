import os
from flask import Flask, request, jsonify
import logging
import time

# 設定日誌
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# 【關鍵改動】我們完全不 import DeepFace
# from deepface import DeepFace 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running! (Ultra-light Test Mode)</h1>"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_face():
    logging.info("=================================")
    logging.info("接收到 /analyze 請求！")

    if 'file' not in request.files:
        logging.error("請求中找不到檔案部分。")
        return jsonify({"error": "file part missing"}), 400

    file = request.files['file']
    logging.info(f"成功獲取檔案: {file.filename}")

    # 為了確保伺服器真的收到了檔案，我們依然儲存它
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(filepath)
        logging.info("✅ 檔案成功儲存到伺服器！")
        
        # 直接回傳一個假的、成功的結果
        dominant_emotion = "test_successful" 
        logging.info(f"✅ (極輕量測試) 回傳 '{dominant_emotion}'。")
        
        os.remove(filepath)
        
        return jsonify({"dominant_emotion": dominant_emotion})

    except Exception as e:
        logging.error(f"伺服器在處理檔案時發生錯誤: {str(e)}")
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "未知的伺服器錯誤"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)