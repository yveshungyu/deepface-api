import os
from flask import Flask, request, jsonify
import logging
import time # Import the time module

# Setup logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Create a folder to temporarily store uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
    return "<h1>DeepFace API is running! (Debug Mode)</h1>"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_face():
    # --- Detailed Logging ---
    logging.info("=================================")
    logging.info("Received request for /analyze!")

    if 'file' not in request.files:
        logging.error("File part missing from request.")
        return jsonify({"error": "file part missing"}), 400

    file = request.files['file']
    logging.info(f"Successfully got file: {file.filename}")

    if file.filename == '':
        logging.error("No file selected.")
        return jsonify({"error": "no file selected"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        try:
            logging.info(f"Attempting to save file to: {filepath}")
            file.save(filepath)
            logging.info("✅ File successfully saved to server!")

            # --- CRITICAL CHANGE: Bypass the resource-intensive DeepFace call ---
            # analysis_result = DeepFace.analyze( ... )
            
            # To simulate work, we'll just pause the program for a moment
            logging.info("Simulating analysis process...")
            time.sleep(2)

            # Return a fake, successful result directly
            dominant_emotion = "neutral" # Dummy result
            logging.info(f"✅ (Simulated) Analysis complete, returning '{dominant_emotion}'.")
            
            os.remove(filepath)
            logging.info("Temporary file deleted from server.")
            
            return jsonify({"dominant_emotion": dominant_emotion})

        except Exception as e:
            logging.error(f"An error occurred while processing the file on the server: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Unknown server error"}), 500

# This block is not executed by Gunicorn but is good practice to keep
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)