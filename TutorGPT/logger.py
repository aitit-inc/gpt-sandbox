import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
log_filename = "output.log"
file_handler = logging.FileHandler(filename=log_filename)
handlers = [stream_handler, file_handler]


class TimeFilter(logging.Filter):
    def filter(self, record):
        return "Running" in record.getMessage()
    

logger.addFilter(TimeFilter())

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(asctime)s - %(levelname)s - %(message)s",
    handlers=handlers
)


def time_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        logger.info(f"Running {func.__name__}")
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"Finished {func.__name__} in {end - start:.3f}s")
        return result
    return wrapper