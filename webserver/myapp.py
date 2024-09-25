from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World from Flask!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # NOTE: the 'file' comes from:
        #  curl -F "file=@requirements.txt" http://localhost/upload
        f = request.files['file']
        f.save(f"./file_uploads/{f.filename}")
        return "file uploaded successfully"
    else:
        return "file form website something?"

@app.route('/download', methods=['GET'])
def download_file():
    return send_file("./file_uploads/requirements.txt" , as_attachment=True)

if __name__ == '__main__':
    app.run()