from flask import render_template, request, send_file, jsonify, redirect, \
    url_for

import urllib
import json
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from myapp import app
from myapp import jwt

from app.database.types_db import ImgObject

from app.post_img import handle_img
from app.text_query import handle_text_query
from app.get_room_img import fs_get_room_img
from app.auth import register_user, login_user, logout_user, check_blocklist
from app.config import Config


# ========================== Page Routes ==========================

# TODO For now, don't use blueprints

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/img_search.html')
@jwt_required()
def img_search():
    return render_template("img_search.html")


# TODO likely change this for frontend
@app.route('/login.html')
def login_page():
    return render_template('login.html')


# TODO likely change this for frontend
@app.route('/register.html')
def register_page():
    return render_template('register.html')

# ========================== Auth Routes ==========================

@app.route('/login', methods=['POST'])
def login():
    uname = request.json.get('username')
    pw = request.json.get('password')

    succ, msg = login_user(uname, pw)

    if not succ:
        return jsonify(msg=msg), 400
    
    # TODO hardcode url bad
    return jsonify(access_token=msg, redirect_url="/"), 200


@app.route('/register', methods=['POST'])
def register():
    # TODO note depending on get or post, could register or render html
    # TODO might user id be helpful to identify user vs. string?

    uname = request.json.get('username')
    pw = request.json.get('password')

    if not register_user(uname, pw):
        return jsonify(msg="User already exists"), 400
    
    return jsonify(msg="User registered successfully", redirect_url="/login"), 200
    # TODO Similarly, you could redirect people to the normal webpage


# TODO logout untested
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jwt = get_jwt()
    logout_user(jwt)
    return jsonify({"msg": "Logout successful"}), 200

# TODO untested
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return check_blocklist(jwt_payload)


# ========================== App Routes ==========================

# TODO add real verification later
# Intended for website text query
@app.route('/text_query')
@jwt_required()
def text_query():
    jwt = get_jwt()
    user = jwt['sub']  # TODO, sanitize inputs? is it ok if thread dies?
    query = request.args.get('query')
    index = request.args.get('index')

    # Simple way to case on stuff to test database, neg num is how many back
    # In the future, can complicate policies to add stuff like auth/security
    response = handle_text_query(user, query, index)
    
    return jsonify(response)

# TODO rename?
# Intended for website to resolve provided image urls
@app.route('/get_room_img', methods=['GET'])
@jwt_required()
def get_room_img():
    jwt = get_jwt()
    user = jwt['sub']

    data_arg = request.args.get('data')
    if data_arg == None:
        # TODO standardize error, msg, etc., whatever
        # TODO standardize where sanitization will be done
        return {"error": "No data parameter provided"}, 400
    
    try:
        decoded_data = urllib.parse.unquote(data_arg)
        db_line_dict = json.loads(decoded_data)
        db_line_obj = ImgObject(**db_line_dict)
    except Exception as e:
        return {"error": "Invalid URL"}, 400
    
    img = fs_get_room_img(user, db_line_obj)

    if img == None:
        return {"error": "Image file not found"}, 400
    
    return send_file(img, download_name=db_line_obj.img_url)
        

# Intended for raspi speech query
@app.route('/speech_query', methods=['POST'])
def speech_query():
    pass

# TODO maybe not code 400? TODO find best?
@app.route('/post_img', methods=['POST'])
@jwt_required()
def post_img():
    jwt = get_jwt()
    user = jwt['sub']  # TODO, sanitize inputs? is it ok if thread dies?
    
    f = request.files['file']
    
    if not handle_img(user, f):
        return {"error": "User not found"}, 400

    return '', 200

# TODO eventually have some way to securly get images
# @app.route('/get_img/<str:file>', methods=['GET'])
# def get_img




# Demo routes: ==============================================================
# TODO delete demo routes

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