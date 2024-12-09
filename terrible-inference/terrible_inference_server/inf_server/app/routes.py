from myapp import app
from flask import request, jsonify
from app.infer_gd import handle_img
import os
import time




@app.route('/ask_abadi', methods=['POST'])
def ask_abadi():

    f = request.files['file']

    texts = request.form.get('texts')

    pathname = f"img_file{os.getpid()}.jpg"
    f.save(pathname)

    print("Received image and texts")
    print("time:", time.time())
    inf_info = handle_img(pathname, texts)
    print("Inference done")
    print("time:", time.time())

    return jsonify(inf_info), 200


@app.route('/', methods=['GET'])
def ret():
    return 'ping', 200