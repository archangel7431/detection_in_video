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
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400
    if file:
        filename = file.filename
        file.save(os.path.join("uploads", filename))
        return jsonify({"message": "file uploaded successfully"}), 200


@app.route("/webcam")
def webcam():
    return render_template("webcam.html")


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run("localhost", debug=True)
