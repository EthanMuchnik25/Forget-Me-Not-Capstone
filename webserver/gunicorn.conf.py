# ABOUT: This file contains the gunicorn hooks, which perform special 
#  functionality outside of the normal flask runtime

import os
from app.perf.perf import init_perf_on_flask_startup, init_perf_on_worker_startup
from app.config import Config
from  app.whisperDownload import download_whisper_model
import whisper


# Runs once when the master Gunicorn process starts. Useful for setting up 
#  resources needed across all workers.
def on_starting(server): 
    # download_whisper_model("small")
    # Initialize performance monitoring on Flask startup
    init_perf_on_flask_startup()


# Runs after each worker is forked. Good for creating per-worker instances of 
#  resources.
def post_fork(server, worker): 
    init_perf_on_worker_startup()

# # Runs when a worker exits. Useful for cleanup.
# def worker_exit(server, worker): 
#     pass

# # Runs when the master process is shutting down. Useful for global cleanup
# def on_exit(server): 
#     pass


timeout = 300  # 5 minutes
graceful_timeout = 300
# NOTE: I think there can also be hooks that trigger on signals, like int, etc.