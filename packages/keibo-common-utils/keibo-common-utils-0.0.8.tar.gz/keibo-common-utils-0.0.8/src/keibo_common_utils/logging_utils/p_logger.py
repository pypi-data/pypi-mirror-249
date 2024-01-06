import os
import logging
import pathlib


# Define default log_file_path
DEFAULT_LOG_FILE_DIR = "/".join(os.path.dirname(__file__).split("/")[:-3])


class P_Logger(logging.Logger):
    logger: logging.Logger

    def __init__(self, log_file_path: str = "", app_name: str = "") -> logging.Logger:
        if app_name != "":
            logger = logging.getLogger(app_name)
        else:
            logger = logging.getLogger()

        logger.setLevel(logging.INFO)

        # Create formatter
        if log_file_path == "":
            log_file_path = os.path.join(DEFAULT_LOG_FILE_DIR, f"{app_name}_logs.txt")
        else:
            path = pathlib.Path(log_file_path)
            path.mkdir(parents=True, exist_ok=True)
            log_file_path = os.path.join(log_file_path, f"{app_name}_logs.txt")

        c_handler = logging.FileHandler(log_file_path, mode="w")
        c_formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
        c_handler.setFormatter(c_formatter)

        # Add handlers to the logger
        logger.addHandler(c_handler)

        self.logger = logger

    def get_logger(self) -> logging.Logger:
        return self.logger
