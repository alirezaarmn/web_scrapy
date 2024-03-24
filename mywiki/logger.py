from flask import jsonify

import json
import logging

class Logger:
    def __init__(self, name, filename, level=logging.DEBUG) -> None:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        handler = logging.FileHandler(filename)        
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def logError(self, raw_json):
        json_object = json.dumps(jsonify(raw_json).json, indent=3)
        self.logger.error(json_object)

    def logDebug(self, raw_json):
        json_object = json.dumps(jsonify(raw_json).json, indent=3)
        self.logger.debug(json_object)
