import logging

from function.my_time import time_date


def logInFile():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    time = time_date()
    log_filename = f"./log/log_{time}.log"
    file = logging.FileHandler(log_filename, encoding='utf-8')
    file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file)
    return logger
