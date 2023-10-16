import logging
import os
from datetime import datetime

_FILE = os.path.dirname(os.path.dirname(__file__))
_FILEPATH = f"{_FILE}/log"
checkFileTime = False
if not checkFileTime:
    time = datetime.now().date()
    checkFileTime = True


def logInFile():
    loggerFile = logging.getLogger(__name__)
    loggerFile.setLevel(logging.DEBUG)
    log_filename = f"{_FILEPATH}/log_{time}.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    loggerFile.addHandler(file)
    return loggerFile


logger = logInFile()
