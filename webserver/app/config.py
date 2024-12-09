# File containing configuration settings for webserver

from datetime import timedelta

# TODO: Add settings to know which components should be mocked
class Config:
    # TODO find uses
    ENV = 'CLOUD' # else 'APP'
    OPENAI_KEY = 'blah'

    # Versions
    YOLO_VER = "V11" # V11, ONNX_YOLO, ONNX_PY, MOCK, DINO, BOTH
    DATABASE_VER = "SQLITE"

    VECTOR_COSINE = "LIGHT-COMPUTE" # HEAVY-COMPUTE, LIGHT-COMPUTE, DOESNT-RUN, would recc LIGHT-COMPUTE for local
    SIMILARITY_THRESHOLD = 0.70 # 0.75 is good for HEAVY-COMPUTE but 0.7 is probably better for LIGHT-COMPUTE

    # For auth
    JWT_SECRET_KEY = "this can sorta be anything"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30) # How long jwt valid for
    JWT_HASH_FN = "pbkdf2"

    PERF = True
    # Where the logs will be spat out
    PERF_LOG_DIR = "./app/perf/logs"
