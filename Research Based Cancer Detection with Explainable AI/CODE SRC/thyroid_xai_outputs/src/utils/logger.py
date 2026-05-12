import logging, sys
from pathlib import Path
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
def setup_logger(name="thyroid_app"):
    lg = logging.getLogger(name)
    if not lg.handlers:
        lg.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s", datefmt="%H:%M:%S")
        sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt); lg.addHandler(sh)
        fh = logging.FileHandler(LOG_DIR / "app.log"); fh.setFormatter(fmt); lg.addHandler(fh)
    return lg
logger = setup_logger()
