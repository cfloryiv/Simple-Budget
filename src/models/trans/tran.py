import uuid
import datetime
import requests
from common.database import Database
from models.control.control import Control

class Trans(object):
    def __init__(self, user_email, name, period, amount, trans_date=None, _id=None):
        self.user_email=user_email
        self.name=name
        self.period=period
        self.amount=float(amount)
        self.trans_date=datetime.datetime.utcnow
        self.trans_date=trans_date if trans_date is None else trans_date
        self._id=uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Account: {}, Period: {}, Amount: {}.".format(self.name, self.period, self.amount)

    def save_to_mongo(self):
        Database.update("trans", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "period": self.period,
            "trans_date": self.trans_date,
            "amount": self.amount,
            "user_email": self.user_email
        }
    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find("trans", {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, trans_id):
        return cls(**Database.find_one("trans", {"_id": trans_id}))

    def delete(self):
        Database.remove("trans", {"_id": self._id})

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('trans', {})]

    @classmethod
    def find_by_account_period(cls, name, period):
        return [cls(**elem) for elem in Database.find("trans", {"name": name, "period": period})]  

    @classmethod
    def find_by_account(cls, name):
        return [cls(**elem) for elem in Database.find("trans", {"name": name})]  
