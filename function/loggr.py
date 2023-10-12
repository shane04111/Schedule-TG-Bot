import logging
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
FILEPATH = os.getenv('FILE')
time = datetime.now().date()


def logInFile():
    loggerFile = logging.getLogger(__name__)
    loggerFile.setLevel(logging.DEBUG)
    log_filename = f"{FILEPATH}/log_{time}.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    loggerFile.addHandler(file)
    return loggerFile


logger = logInFile()
