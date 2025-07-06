import os
import flask
from flask import request, jsonify
import logging
import base64
import numpy as np
import cv2
from deepface import DeepFace # 我們把 DeepFace 重新加回來！

logging.basicConfig(level=logging.INFO)
app = flask.Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running! (Production Mode)</h1>"

@app.route('/analyze', methods=['POST'])
def analyze_face():
    logging.info("=================================")
    logging.info("Received request for /analyze (Production Mode)!")
    
    try:
        data = request.get_json()
        if 'image_base64' not in data:
            return jsonify({"error": "Missing image_base64 in JSON payload"}), 400
            
        # 將 Base64 字串解碼回圖片的二進位資料
        image_data = base64.b64decode(data['image_base64'])
        
        # 將二進位資料轉換成 OpenCV 可以讀取的格式
        np_arr = np.frombuffer(image_data, np.uint8)
        img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 執行真正的 DeepFace 情緒分析
        logging.info("Starting DeepFace analysis...")
        analysis_result = DeepFace.analyze(
            img_path=img_np, 
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='retinaface' # 使用一個輕量級的偵測器
        )
        
        # DeepFace 的結果是一個列表，我們取第一個偵測到的臉
        dominant_emotion = analysis_result[0]['dominant_emotion']
        logging.info(f"✅ DeepFace analysis complete! Dominant emotion: {dominant_emotion}")
        
        return jsonify({"dominant_emotion": dominant_emotion})

    except Exception as e:
        logging.error(f"An error occurred during analysis: {str(e)}")
        # 傳回詳細錯誤，方便除錯
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)