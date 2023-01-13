"""Artifact.py - describes one piece of data that is saved to this machine. """

import datetime
import json

# TODO - have each Artifact consist of multiple "pages" of data
class Artifact:
    filename = ""
    importance = -1
    timestamp = None

    def __int__(self, importance=-1, filename=""):
        self.timestamp = datetime.datetime.now()
        self.importance = importance
        self.filename = filename

    def to_json(self):
        attr_dict = {}
        attr_dict["timestamp"] = datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        attr_dict["importance"] = self.importance
        attr_dict["filename"] = self.filename

        return json.dumps(attr_dict)
