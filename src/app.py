from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("websitenew.html")


@app.route("/process-file", methods=["POST"])
def process_file():
    file_path = request.form.get("filePath")

    # result = subprocess.run(
    #     ["python", ".\src\final.py", file_path], capture_output=True, text=True)

    # output = result.stdout

    print(f"Received file path: {file_path}")

    return jsonify({"Message": "File path receieved and processed"})


if __name__ == "__main__":
    app.run()
