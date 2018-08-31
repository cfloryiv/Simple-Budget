import uuid
import datetime
import requests
from common.database import Database

class Account(object):
    def __init__(self, user_email, name, budget, _id=None):
        self.user_email=user_email
        self.name=name
        self.budget=float(budget)
        self._id=uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Account: {}, Budget: {}.".format(self.name, self.budget)

    def save_to_mongo(self):
        Database.update("accounts", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "budget": self.budget,
            "user_email": self.user_email
            }

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find("accounts", {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, account_id):
        return cls(**Database.find_one("accounts", {"_id": account_id}))

    def delete(self):
        Database.remove("accounts", {"_id": self._id})
    
    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('accounts', {})]

    @classmethod
    def find_by_name(cls, name):
        return cls(**Database.find_one("accounts", {"name": name}))
