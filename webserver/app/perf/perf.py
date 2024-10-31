import logging
import os
import time
import app.perf.helpers as helpers
from app.config import Config
from functools import wraps

PERF_LEVEL = 5
perf_pid = os.getpid()


# This is not intended to be called outside time_and_log. It gets something 
#  specific on the stack frame.
def perf(self, fn_name, fn_time):
    if self.isEnabledFor(PERF_LEVEL) and Config.PERF:
        # NOTE: I am not sure if the behavior of this is documented but it seems
        #  to work?
        self._log(PERF_LEVEL, "%d %s %f", (perf_pid, fn_name, fn_time))



# Set up logger for decorator, if performance monitoring is on:==============

if Config.PERF:
    # NOTE:
    # Log folders, located in webserver/app/perf/logs, contain all logs for a single
    #  run of the server. This function determines the name of the next log folder.
    #  It should be 1 greater than the last log directory.
    # The log folder is made in gunicorn.conf.py, this just finds it
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


# IMPORTANT:: Decorator:=======================

# This is the only thing you should import

# Decorator to calculate duration taken by any function.
def time_and_log(func):

    if not Config.PERF:
        return func
    
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    @wraps(func)
    def inner1(*args, **kwargs):

        # storing time before function execution
        begin = time.time()
        
        result = func(*args, **kwargs)

        # storing time after function execution
        end = time.time()
        logger.perf(func.__name__, end-begin)

        return result
        
    return inner1


