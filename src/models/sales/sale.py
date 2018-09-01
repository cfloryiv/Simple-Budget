import uuid
import datetime
import requests
from common.database import Database
from models.control.control import Control

class Sale(object):
    def __init__(self, name, period, budget, sales, _id=None):
        self.name=name
        self.period=period
        self.budget=float(budget)
        self.sales=sales
        self._id=uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Account: {}, Period {}, Sales: {}".format(self.name, self.period, self.sales)

    def save_to_mongo(self):
        Database.update("sales", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "period": self.period,
            "budget": self.budget,
            "sales": self.sales
            }

    @classmethod
    def find_by_account_period(cls, name, period):
        sale=Database.find_one("sales", {"name": name, "period": period})
        if sale==None:
            sale=Sale("new", "1234-12", 0.0, 0.0)
            return sale
        else:
            return cls(**sale)

    @classmethod
    def find_by_id(cls, account_id):
        return cls(**Database.find_one("sales", {"_id": account_id}))

    def delete(self):
        Database.remove("sales", {"_id": self._id})
    
    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find('sales', {})]

    @classmethod
    def find_by_period(cls):
        control=Control.find_by_id('misc')
        period=control.period[0][0]
        return [cls(**elem) for elem in Database.find('sales', {"period": period})]

    @classmethod
    def find_by_periods(cls):
        sales=Sale.all()
        amounts={}
        for sale in sales:
            if sale.period in amounts:
                amounts[sale.period][0]+=sale.budget
                amounts[sale.period][1]+=sale.sales
            else:
                amounts[sale.period]={}
                amounts[sale.period][0]=sale.budget
                amounts[sale.period][1]=sale.sales
        return amounts
            
