import logging
import os

from dotenv import load_dotenv

from src.function.my_time import myTime

load_dotenv()
_FILE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_FILEPATH = f"{_FILE}/log"


def logInFile():
    logger_file = logging.getLogger(__name__)
    level = logging.INFO
    if eval(os.getenv('DEBUG')):
        level = logging.DEBUG
    logger_file.setLevel(level)
    log_filename = f"{_FILEPATH}/log.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger_file.addHandler(file)
    return logger_file


def logFinal():
    log_suffix = ""
    log_file_name = f"{_FILEPATH}/log_{myTime().date()}{log_suffix}.log"
    counter = 1
    while os.path.isfile(log_file_name):
        log_suffix = f"_{counter}"
        log_file_name = f"{_FILEPATH}/log_{myTime().date()}{log_suffix}.log"
        counter += 1
    os.rename(f"{_FILEPATH}/log.log", log_file_name)


logger = logInFile()
