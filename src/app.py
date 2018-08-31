from flask import Flask, render_template
from common.database import Database

__author__ = 'cfloryiv'


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')

from models.users.views import user_blueprint
from models.accounts.views import account_blueprint
from models.trans.views import trans_blueprint
from models.sales.views import sales_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(account_blueprint, url_prefix="/accounts")
app.register_blueprint(trans_blueprint, url_prefix="/trans")
app.register_blueprint(sales_blueprint, url_prefix='/sales')
