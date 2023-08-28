from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import os
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filename = file.filename
        file.save(os.path.join("uploads", filename))
        return jsonify({"message": "file uploaded successfully"}), 200

@app.route("/webcam")
def webcam():
    return render_template("webcam.html")        

@app.route("/video_feed")
def video_feed():
    cap = cv2.VideoCapture(0)
    n = 0
    while True:
        n += 1
        ret, frame = cap.read()
        if ret:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            print(f"Getting image: {n}")
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
        cap.release()

if __name__ == "__main__":
    # if not os.path.exists("uploads"):
    #     os.makedirs("uploads")
    app.run("localhost", debug=True)
