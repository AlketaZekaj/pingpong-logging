import os
import requests
import uuid
from datetime import datetime
import time
from flask import Flask, jsonify
import threading

app = Flask(__name__)
log_output = ""

# Config and env
INFO_FILE_PATH = "/config/information.txt"
MESSAGE = os.getenv("MESSAGE", "No message set")
PINGPONG_URL = os.getenv(
    "PINGPONG_URL", "http://pingpong-service:5000/pingpong"
)

# Background thread to generate log lines
def generate_logs():
    global log_output
    while True:
        try:
            with open(INFO_FILE_PATH) as f:
                file_content = f.read().strip()
        except Exception as e:
            file_content = f"Error reading file: {e}"

        try:
            res = requests.get(PINGPONG_URL)
            count = res.json().get("pong_count", "?")
        except Exception as e:
            count = f"Error: {e}"

        log_line = (
            f"file content: {file_content}\n"
            f"env variable: MESSAGE={MESSAGE}\n"
            f"{datetime.utcnow().isoformat()}: {uuid.uuid4()}\n"
            f"Ping / Pongs: {count}"
        )
        print(log_line)
        log_output = log_line
        time.sleep(5)

@app.route("/")
def health():
    return "OK", 200

@app.route('/status')
def status():
    return jsonify({"output": log_output})

if __name__ == '__main__':
    threading.Thread(target=generate_logs, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)