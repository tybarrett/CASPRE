"""ArtifactRecord.py - describes one piece of data (not on the current machine) """

import datetime
import json


class Artifact:
    host = ""
    importance = -1
    timestamp = None

    def __int__(self, importance=-1, host=""):
        self.timestamp = datetime.datetime.now()
        self.importance = importance
        self.host = host

    def to_json(self):
        attr_dict = {}
        attr_dict["timestamp"] = datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        attr_dict["importance"] = self.importance
        attr_dict["host"] = self.host

        return json.dumps(attr_dict)
