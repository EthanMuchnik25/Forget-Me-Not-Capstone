# File containing configuration settings for webserver

from datetime import timedelta

# TODO: Add settings to know which components should be mocked
class Config:
    # TODO find uses
    ENV = 'CLOUD' # else 'APP'
    OPENAI_KEY = 'blah'

    # Versions
    YOLO_VER = "DINO" # V11, ONNX_YOLO, ONNX_PY, MOCK, DINO, BOTH
    DATABASE_VER = "SQLITE"

    VECTOR_COSINE = "LIGHT-COMPUTE" # HEAVY-COMPUTE, LIGHT-COMPUTE, DOESNT-RUN, would recc LIGHT-COMPUTE for local
    SIMILARITY_THRESHOLD = 0.70 # 0.75 is good for HEAVY-COMPUTE but 0.7 is probably better for LIGHT-COMPUTE
    VECTOR_COSINE_REMOTE_IP = '172.24.156.5'
    VECTOR_COSINE_REMOTE_ENDPOINT = f'http://{VECTOR_COSINE_REMOTE_IP}:3999/similar_vector_compute'
    TRANSCRIBE_REMOTE_IP = '172.24.156.5'
    TRANSCRIBE_REMOTE_ENDPOINT = f'http://{TRANSCRIBE_REMOTE_IP}:3999/transcribe'

    # For auth
    JWT_SECRET_KEY = "this can sorta be anything"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30) # How long jwt valid for
    JWT_HASH_FN = "pbkdf2"

    # Whisper model to load
    WHISPER_MODEL = "medium" # "base" or "tiny"

    PERF = True
    # Where the logs will be spat out
    PERF_LOG_DIR = "./app/perf/logs"

    #EXTRA FEATURES
    PRUNING = False
    MSE_THRESHOLD = 0.28

