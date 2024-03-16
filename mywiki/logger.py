from enum import Enum
from flask import jsonify

import json
import time
import logging

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class Logger:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                            format='%(name)s , %(levelname)s, %(message)s')

    def log(self, loglevel, status, raw_json):

        # check the file size and save json file 
        json_object = json.dumps(jsonify(
                                epoc = time.time(), 
                                loglevel = loglevel.name,
                                status = status,
                                message=raw_json).json, indent=3)

        print(json_object)
        # Writing to sample.json
        # logging.info(json_object)
        # with open("sample.json", "w") as outfile:
        #     outfile.write(json_object)

