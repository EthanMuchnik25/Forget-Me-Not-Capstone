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
from app.auth import register_user, login_user, logout_user, \
    check_jwt_not_blocklist, deregister_user
from app.config import Config
from app.perf.perf import time_and_log


# ========================== Page Routes ==========================

# TODO For now, don't use blueprints

@app.route('/')
@time_and_log
def hello_world():
    return render_template("index.html")


@app.route('/img_search.html')
# @jwt_required() # Fuck. The alternative is tragic. See index.html
@time_and_log
def img_search():
    return render_template("img_search.html")


# TODO likely change this for frontend
@app.route('/login.html')
@time_and_log
def login_page():
    return render_template('login.html')


# TODO likely change this for frontend
@app.route('/register.html')
@time_and_log
def register_page():
    return render_template('register.html')

# ========================== Auth Routes ==========================

@app.route("/test_auth")
@jwt_required()
@time_and_log
def test_auth():
    return jsonify(msg="Authentication successful"), 200

@app.route('/login', methods=['POST'])
@time_and_log
def login():
    uname = request.json.get('username')
    pw = request.json.get('password')

    succ, msg = login_user(uname, pw)

    if not succ:
        return jsonify(msg=msg), 400
    
    # TODO hardcode url bad
    # TODO originally brought you back to main page bc img_search.html did not
    #  exist
    return jsonify(access_token=msg, redirect_url="/img_search.html"), 200


@app.route('/register', methods=['POST'])
@time_and_log
def register():
    # TODO note depending on get or post, could register or render html
    # TODO might user id be helpful to identify user vs. string?

    uname = request.json.get('username')
    pw = request.json.get('password')

    if not register_user(uname, pw):
        return jsonify(msg="User already exists"), 400
    
    return jsonify(msg="User registered successfully", redirect_url="/login.html"), 200
    # TODO Similarly, you could redirect people to the normal webpage


# TODO logout untested
@app.route('/logout', methods=['POST'])
@jwt_required()
@time_and_log
def logout():
    jwt = get_jwt()
    logout_user(jwt)
    return jsonify(msg="Logout successful"), 200


@app.route('/deregister', methods=['POST'])
@jwt_required()
@time_and_log
def deregister():
    jwt = get_jwt()
    uname = jwt['sub']
    # this should also invalidate tokens
    deregister_user(uname)
    return jsonify(msg="Account deleted successruly", redirect_url="/register.html"), 200


# TODO untested
# TODO remove for now
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return check_jwt_not_blocklist(jwt_payload)


# ========================== App Routes ==========================

# TODO add real verification later
# Intended for website text query
@app.route('/text_query')
@jwt_required()
@time_and_log
def text_query():
    jwt = get_jwt()
    user = jwt['sub']  # TODO, sanitize inputs? is it ok if thread dies?
    query = request.args.get('query')
    index = request.args.get('index')

    # Simple way to case on stuff to test database, neg num is how many back
    # In the future, can complicate policies to add stuff like auth/security
    response = handle_text_query(user, query, index)

    return jsonify(response), 200

# TODO logger functionality is shit. Refacror code so we don't have to be so 
#  careful
# TODO rename?
# Intended for website to resolve provided image urls
@app.route('/get_room_img', methods=['GET'])
@jwt_required()
@time_and_log
def get_room_img():
    jwt = get_jwt()
    user = jwt['sub']

    data_arg = request.args.get('data')
    if data_arg == None:
        # TODO standardize error, msg, etc., whatever
        # TODO standardize where sanitization will be done
        ret = {"error": "No data parameter provided"}, 400
    
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
        

# TODO maybe not code 400? TODO find best?
@app.route('/post_img', methods=['POST'])
@jwt_required()
@time_and_log
def post_img():
    jwt = get_jwt()
    user = jwt['sub']  # TODO, sanitize inputs? is it ok if thread dies?
    
    f = request.files['file']
    
    if not handle_img(user, f):
        return {"error": "User not found"}, 400

    return '', 200

@app.route('/get_username', methods=['GET'])
@jwt_required()
@time_and_log
def get_username():
    jwt = get_jwt()
    user = jwt['sub']

    return {"username": user}, 200


@app.route('/speech_query', methods=['POST'])
@jwt_required()
@time_and_log
def speech_query():
    # NOTE: This is a dummy response. Ethan if you decide to code this up put
    #  it all in a different file, maybe like speech.py or something

    query = request.args.get('query')
    if query == None:
        return {"msg": "You forgot to include query in your body"}, 200

    return {"msg": "Good job champ you will definitely find your thing"}, 200


