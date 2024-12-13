from myapp import app
from flask import request, jsonify
from app.infer_gd import handle_img
from app.speech_compute import getMostSimilar
import os
import time
import numpy as np
import whisper

model = None

@app.before_request
def load_models():
    global model
    model = whisper.load_model("base.en")
    print("Model loaded and ready to serve requests")

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

@app.route('/similar_vector_compute', methods=['POST'])
def similar_vector_compute():

    data = request.get_json()
    query = data['query']
    wordList = data['wordList']

    closestName = getMostSimilar(query, wordList)
    return {"closestName": closestName}, 200

@app.route('/transcribe', methods=['POST'])
def transcribe():

    data = request.get_json()
    audio_chunk = data['audio_chunk']

    audio_chunk = np.array(audio_chunk)
    audio_chunk = audio_chunk.astype(np.float32)


    global model

    result = model.transcribe(audio_chunk, fp16=False, language='en', no_speech_threshold=0.4)
    transcribed_text = result["text"].strip().lower()
    # print("transcribed text is: ", transcribed_text)
    
    response = {'text': transcribed_text}
    print("transcribed text is: ", transcribed_text)

    return jsonify(response), 200


@app.route('/', methods=['GET'])
def ret():
    return 'ping', 200