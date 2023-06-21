from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)


@app.route("/")
def home():
    return render_template("websitenew.html")

@app.route('/data', methods=['GET'])
def get_data():
    # Process the request and generate a response
    data = {'message': 'Hello from Flask server!'}
    return jsonify(data)



if __name__ == "__main__":
    app.run()
