import os
import flask
from flask import request, jsonify
import logging
import base64 # 新增 base64 函式庫

logging.basicConfig(level=logging.INFO)
app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running! (Base64 Mode)</h1>"

@app.route('/analyze', methods=['POST'])
def analyze_face():
    logging.info("=================================")
    logging.info("Received request for /analyze (Base64)!")
    
    try:
        # 從 JSON 中獲取 base64 字串
        data = request.get_json()
        if 'image_base64' not in data:
            return jsonify({"error": "Missing image_base64 in JSON payload"}), 400
            
        # 我們甚至可以不做任何事，直接回傳成功，來確認連線
        dominant_emotion = "base64_test_successful"
        logging.info(f"✅ (Base64 Test) Successfully received JSON data, returning '{dominant_emotion}'.")
        
        return jsonify({"dominant_emotion": dominant_emotion})

    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)