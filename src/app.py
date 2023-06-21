from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("websitenew.html")

@app.route('/data', methods=['GET'])
def get_data():
    # Process the request and generate a response
    data = {'message': 'Hello from Flask server!'}
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            # Process the file as needed
            # Example: Save the file to the current directory
            file.save(file.filename)
            return 'File uploaded successfully.'
    # If no file was uploaded or GET request, render the HTML form
    return render_template('websitenew.html')


if __name__ == "__main__":
    app.run()
