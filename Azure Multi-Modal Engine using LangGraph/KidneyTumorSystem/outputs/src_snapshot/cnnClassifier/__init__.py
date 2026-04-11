import os, sys, logging

_LOG_FMT  = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
_LOG_DIR  = "logs"
_LOG_FILE = os.path.join(_LOG_DIR, "running_logs.log")
os.makedirs(_LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=_LOG_FMT,
    handlers=[
        logging.FileHandler(_LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("cnnClassifierLogger")
