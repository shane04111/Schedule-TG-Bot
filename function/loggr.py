import logging
import os

from dotenv import load_dotenv
from function.my_time import time_date
load_dotenv()
FILEPATH = os.getenv('FILE')


def logInFile():
    loggerFile = logging.getLogger(__name__)
    loggerFile.setLevel(logging.DEBUG)
    time = time_date()
    log_filename = f"{FILEPATH}/log_{time}.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    loggerFile.addHandler(file)
    return loggerFile


logger = logInFile()
