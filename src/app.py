from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os

from final import motion_detection


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


@app.route("/set_roi", methods=["POST"])
def set_roi():
    data = request.get_json()
    roi_wanted = False

    if data["roi"]:
        roi_wanted = True

    return jsonify({"roi_wanted": roi_wanted}), 200


@app.route("/processed_video/<filename>", methods=["POST"])
def processed_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# @app.route("/webcam")
# def webcam():
#     return render_template("webcam.html")


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run("localhost", debug=True)
