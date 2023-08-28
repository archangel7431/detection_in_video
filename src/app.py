from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("websitenew.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filename = file.filename
        file.save(os.path.join("uploads", filename))
        return jsonify({"message": "file uploaded successfully"}), 200

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run("localhost", debug=True)
