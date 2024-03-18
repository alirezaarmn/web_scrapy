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
    def __init__(self, filename) -> None:
        logging.basicConfig(level=logging.DEBUG, filename=filename, filemode='w')
        pass

    def logError(self, raw_json):
        json_object = json.dumps(jsonify(raw_json).json, indent=3)
        logging.error(json_object)

    def logDebug(self, raw_json):
        json_object = json.dumps(jsonify(raw_json).json, indent=3)
        logging.debug(json_object)
