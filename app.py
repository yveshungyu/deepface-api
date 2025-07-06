import os
from flask import Flask, request, jsonify
from deepface import DeepFace
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# 建立一個資料夾來暫存上傳的圖片
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running!</h1><p>請發送 POST 請求到 /analyze 來分析圖片。</p>"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_face():
    # 檢查請求中是否有檔案
    if 'file' not in request.files:
        return jsonify({"error": "請求中找不到檔案部分 (file part missing)"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "沒有選擇檔案 (no file selected)"}), 400

    if file:
        try:
            # 儲存上傳的檔案
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            logging.info(f"檔案已儲存至: {filepath}")

            # 使用 DeepFace 進行分析
            # 我們只啟用情緒分析，以加快速度
            analysis_result = DeepFace.analyze(
                img_path=filepath, 
                actions=['emotion'],
                enforce_detection=False # 如果找不到臉部，不要拋出錯誤
            )
            
            # DeepFace 的結果是一個列表，我們取第一個元素
            dominant_emotion = analysis_result[0]['dominant_emotion']
            logging.info(f"分析結果: {dominant_emotion}")

            # 刪除暫存檔案
            os.remove(filepath)

            # 回傳結果
            return jsonify({"dominant_emotion": dominant_emotion})

        except Exception as e:
            # 如果 DeepFace 找不到臉部或發生其他錯誤
            logging.error(f"分析時發生錯誤: {str(e)}")
            # 嘗試刪除檔案，以防出錯時檔案還留著
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "未知的伺服器錯誤"}), 500

if __name__ == '__main__':
    # 在本機測試時使用
    app.run(host='0.0.0.0', port=5000)