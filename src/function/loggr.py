import logging
import os

from src.function.my_time import time_date

_FILE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_FILEPATH = f"{_FILE}/log"


def logInFile():
    loggerFile = logging.getLogger(__name__)
    loggerFile.setLevel(logging.DEBUG)
    log_filename = f"{_FILEPATH}/log.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    loggerFile.addHandler(file)
    return loggerFile


def logFinal():
    logSuffix = ""
    logFileName = f"{_FILEPATH}/log_{time_date()}{logSuffix}.log"
    counter = 1
    while os.path.isfile(logFileName):
        logSuffix = f"_{counter}"
        logFileName = f"{_FILEPATH}/log_{time_date()}{logSuffix}.log"
        counter += 1
    os.rename(f"{_FILEPATH}/log.log", logFileName)


logger = logInFile()
