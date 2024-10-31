# ABOUT: This file contains the gunicorn hooks, which perform special 
#  functionality outside of the normal flask runtime

import os
import app.perf.helpers as helpers
from app.config import Config


# Runs once when the master Gunicorn process starts. Useful for setting up 
#  resources needed across all workers.
def on_starting(server): 
    # Set up folders if we want to log
    if Config.PERF:
        next_dir_number = helpers.get_max_log_dir_num(Config.PERF_LOG_DIR) + 1

        new_log_dir = os.path.join(Config.PERF_LOG_DIR, str(next_dir_number))

        # Create the new log directory
        os.makedirs(new_log_dir)
        os.chmod(new_log_dir, 0o777)


# # Runs after each worker is forked. Good for creating per-worker instances of 
# #  resources.
# def post_fork(server, worker): 
#     pass

# # Runs when a worker exits. Useful for cleanup.
# def worker_exit(server, worker): 
#     pass

# # Runs when the master process is shutting down. Useful for global cleanup
# def on_exit(server): 
#     pass



# NOTE: I think there can also be hooks that trigger on signals, like int, etc.