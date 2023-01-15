from os import path
import os
from datetime import datetime
import logging
import warnings
from utilities import file_util

# Temporary Global log directory
log_directory = path.abspath("./logs")
date_format = "%b-%d-%Y_%H-%M"
warnings.warn("deprecated", DeprecationWarning)
warnings.filterwarnings("error")


def start_log(log_level):
    try:
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        now = datetime.now()
        now_formated = now.strftime(date_format)
        log_name = now_formated + ".log"
        file_path = path.abspath(log_directory + "/" + log_name)
        logging.basicConfig(filename=file_path,
                            encoding='utf-8', level=log_level)
    except BaseException as error:
        print("Error excecuting main", error)
        print("Error type", type(error))


def debug(message):
    logging.debug(message)


def info(message):
    logging.info(message)


def warning(message):
    logging.warning(message)


def error(message):
    logging.error(message)
