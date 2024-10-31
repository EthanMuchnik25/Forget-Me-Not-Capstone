import logging
import os
import time
import app.perf.helpers as helpers
from app.config import Config
import inspect

PERF_LEVEL = 5
perf_pid = os.getpid()

class PerfFormatter(logging.Formatter):
    def format(self, record):
        # Add the PID to the log record
        record.pid = perf_pid
        record.unix_time = time.time()
        # TODO: This is awful genuinely atrocious brittle garbage shit
        record.func = inspect.currentframe().f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_code.co_name

        return super().format(record)

def perf(self, *args, **kwargs):
    if self.isEnabledFor(PERF_LEVEL) and Config.LOGGING:
        self._log(PERF_LEVEL, "", args, **kwargs)

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

formatter = PerfFormatter('%(pid)d %(func)s %(unix_time)s %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# logger.perf("this is a test message")

