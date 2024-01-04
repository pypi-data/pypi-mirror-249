import datetime
import logging
from pathlib import Path

LOG_FOLDER = "logs"


def set_logger(filename: str = "", loglevel: int = logging.INFO) -> logging.Logger:
    if filename:
        filename += " "
    Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)
    path = Path(LOG_FOLDER) / f"{filename}{datetime.datetime.now():%Y.%m.%d %H.%M}.log"
    formatter = logging.Formatter(
        "[%(asctime)s] <%(levelname)s> (%(name)s) %(message)s"
    )

    handler_stdout = logging.StreamHandler()
    handler_stdout.setFormatter(formatter)
    handler_stdout.setLevel(loglevel)

    handler_file = logging.FileHandler(str(path), mode="w")
    handler_file.setFormatter(formatter)
    handler_file.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler_file)
    root_logger.addHandler(handler_stdout)
    root_logger.setLevel(logging.DEBUG)
    return root_logger
