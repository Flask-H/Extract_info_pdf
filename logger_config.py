import logging
from pathlib import Path

def get_logger(name="APP"):

    # Carpeta logs junto al proyecto
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "app.log"

    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger
