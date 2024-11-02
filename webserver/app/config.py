# File containing configuration settings for webserver

from datetime import timedelta

# TODO: Add settings to know which components should be mocked
class Config:
    # TODO find uses
    ENV = 'CLOUD' # else 'APP'
    OPENAI_KEY = 'blah'

    # Versions
    YOLO_VER = "V11"
    DATABASE_VER = "SQLITE"

    # For auth
    JWT_SECRET_KEY = "this can sorta be anything"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30) # How long jwt valid for
    JWT_HASH_FN = "pbkdf2"

    PERF = True
    # Where the logs will be spat out
    PERF_LOG_DIR = "./app/perf/logs"
