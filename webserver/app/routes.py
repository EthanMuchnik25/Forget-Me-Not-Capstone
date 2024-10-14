from flask import render_template, request, send_file, jsonify
from myapp import app

# For now, don't use blueprints

@app.route('/')
def hello_world():
    return render_template('img_search.html')


# TODO These are temporary routes. Shore up design later on in accordance with
#  UI decisions

# Intended for website text query
@app.route('/text_query')
def text_query():
    query = request.args.get('query')
    # Simple way to case on stuff to test database, neg num is how many back
    # In the future, can complicate policies to add stuff like auth/security
    index = request.args.get('index')
    if query == 'swaglab':
        response = {
            'imageUrl': '/static/swaglab.jpg',
            'success': True
        }
    elif query == 'sign':
        response = {
            'imageUrl': 'https://i.redd.it/87xuofmvnlud1.png',
            'success': True
        }
    else:
        response = {
            'success': False,
            'message': 'random message'
        }
    return jsonify(response)

# Intended for raspi speech query
@app.route('/speech_query', methods=['POST'])
def speech_query():
    pass

@app.route('/post_img', methods=['POST'])
def post_img():
    f = request.files['file']

    f.save("file_uploads/swaglab.jpg")
    print("file recieved from camera")

    # TODO safe file to database, figure out how it will be structured
    # We have the chatgpt thing to read from database, take inspiration or ask 
    #  again. Once we have the interface it is easily mockable I think, both in
    #  case of local database and remote unauthenticated database. 

    # Much discussion must be done regarding authenticating all transactions vs.
    #  building drastically different architecture for both. 
    # Architecture may not have to be so drastic, can make in such a way that by
    #  having certain options, we bypass the real auth checks. However, cloud
    #  modules require them.

    return '', 400

# TODO eventually have some way to securly get images
# @app.route('/get_img/<str:file>', methods=['GET'])
# def get_img




# Demo routes: ==============================================================

# Example for file upload
@app.route('/upload_test', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # NOTE: the 'file' comes from:
        #  curl -F "file=@requirements.txt" http://localhost/upload
        f = request.files['file']
        f.save(f"./file_uploads/{f.filename}")
        return "file uploaded successfully"
    else:
        return "file form website something?"

# Example for file send
@app.route('/download_test', methods=['GET'])
def download_file():
    return send_file("./file_uploads/requirements.txt" , as_attachment=True)

# Example for query argument parsing
# Query:  fetch(`/search?query=${query}&index=${index}`)
@app.route('/search', )
def search():
    # implicit get function
    query = request.args.get('query')
    index = request.args.get('index')

    if query == 'a':
        response = {
            'query': query,
            'index': index if index is not None else 'default_value',
            'success': True,
            'imageUrl': 'https://i.redd.it/87xuofmvnlud1.png'
        }
    else:
        response = {
            'query': query,
            'success': False,
            'message': 'go fuck yourself'
        }
        return response, 404 # error code example
    return jsonify(response)

# Example you can pattern match on url type
@app.route('/file_never_pick_this/<int:file_id>', methods=['GET'])
def serve_file(file_id):
    return '', 404