from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "src/res/database"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return "File uploaded successfully", 200


# @app.route("/webcam")
# def webcam():
#     return render_template("webcam.html")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run("localhost", debug=True)
