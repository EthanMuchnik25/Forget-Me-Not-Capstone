import logging
import os
import time
import app.perf.helpers as helpers
from app.config import Config
from functools import wraps

PERF_LEVEL = 5
perf_pid = os.getpid()


# ================== Set up environment for perf monitoring ================

# This logs a function with an associated time
def perf(self, fn_name, fn_time):
    if self.isEnabledFor(PERF_LEVEL) and Config.PERF:
        # NOTE: I am not sure if the behavior of this is documented but it seems
        #  to work?
        self._log(PERF_LEVEL, "%d %s %f", (perf_pid, fn_name, fn_time))


# IMPORTANT:: Decorator:=======================

# Decorator to calculate duration taken by any function if perf is enabled.
def time_and_log(func):

    if not Config.PERF:
        return func
    
    # Flask doesn't like it when all the top-level functions are called the 
    #  same thing. This decorator renames it to the name of the fn time_and_log
    #  wraps around.
    @wraps(func)
    def inner1(*args, **kwargs):
        begin = time.time()
        
        result = func(*args, **kwargs)

        end = time.time()
        logger.perf(func.__name__, end-begin)

        return result
        
    return inner1

# IMPORTANT:: To run on server initialization - before many workers

def init_perf_on_flask_startup():
    if Config.PERF:
        next_dir_number = helpers.get_max_log_dir_num(Config.PERF_LOG_DIR) + 1

        new_log_dir = os.path.join(Config.PERF_LOG_DIR, str(next_dir_number))

        # Create the new log directory
        os.makedirs(new_log_dir)
        os.chmod(new_log_dir, 0o777)

def init_perf_on_worker_startup():
    global logger
    # Set up logger for decorator, if performance monitoring is on:
    if Config.PERF:
        proc_perf_log_dir = os.path.join(Config.PERF_LOG_DIR, str(helpers.get_max_log_dir_num(Config.PERF_LOG_DIR)))

        # The file in which this worker's log should be located will be named by it's 
        #  PID.
        perf_log = os.path.join(proc_perf_log_dir, f"{perf_pid}.log")

        logging.addLevelName(PERF_LEVEL, "PERF")
        logging.Logger.perf = perf

        logger = logging.getLogger("perf")
        logger.setLevel(PERF_LEVEL)

        file_handler = logging.FileHandler(perf_log)
        file_handler.setLevel(PERF_LEVEL)
        os.chmod(perf_log, 0o666)

        logger.addHandler(file_handler)
