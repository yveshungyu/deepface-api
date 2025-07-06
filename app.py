import os
from flask import Flask, request, jsonify
import logging
import time

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running! (Ultra-light Test Mode)</h1>"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_face():
    logging.info("Received request for /analyze!")
    if 'file' not in request.files:
        return jsonify({"error": "file part missing"}), 400

    # 為了測試，我們甚至不儲存檔案，直接回傳成功
    dominant_emotion = "test_successful" 
    logging.info(f"✅ (Ultra-light test) Returning '{dominant_emotion}'.")
    return jsonify({"dominant_emotion": dominant_emotion})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)