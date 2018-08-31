import uuid
import datetime
import requests
from common.database import Database

class Control(object):
    def __init__(self, period, _id):
        self.period=period,
        self._id=_id

    def __repr__(self):
        return "<Period: {},".format(self.period)

    def save_to_mongo(self):
        Database.update("control", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "period": self.period
            }


    @classmethod
    def find_by_id(cls, control_id):
        return cls(**Database.find_one("control", {"_id": control_id}))

    def delete(self):
        Database.remove("control", {"_id": self._id})
    
    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('control', {})]
