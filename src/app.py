from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("websitenew.html")


@app.route("/data", methods=["GET"])
def get_data():
    print("GET MESSAGE!!!")

    return jsonify({"Message": "Hello from Flask server!"})


if __name__ == "__main__":
    app.run()
