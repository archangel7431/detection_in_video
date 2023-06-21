from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename="server.log", level=logging.DEBUG)


@app.route("/")
def home():
    return render_template("websitenew.html")


@app.route('/data', methods=['GET'])
def get_data():
    # Process the request and generate a response
    data = {'message': 'Hello from Flask server!'}
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Accessing all headers
    logging.debug('Request Headers:')
    for header, value in request.headers.items():
        logging.debug(f"{header}: {value}")

    logging.debug('Request JSON Payload:')
    logging.debug(request.get_json())


    uploaded_file = request.files['data']
    uploaded_file.save(uploaded_file.filename)  # Save the file to disk
    # Process the uploaded file here
    # Add your file processing logic

    return 'Upload endpoint'

if __name__ == "__main__":
    app.run()
