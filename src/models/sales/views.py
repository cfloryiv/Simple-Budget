from flask import Blueprint, request, render_template, session, redirect, url_for
from models.accounts.account import Account

account_blueprint=Blueprint('accounts', __name__)

@account_blueprint.route('/new', methods=['GET', 'POST'])
def create_account():
    if request.method=='POST':
        name=request.form['name']
        budget=float(request.form['budget'])

        account=Account(session['email'], name, budget).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("accounts/new_account.jinja2")

@account_blueprint.route('/edit/<string:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    if request.method=='POST':
        name=request.form['name']
        budget=float(request.form['budget'])

        account=Account.find_by_id(account_id)
        account.name=name
        account.budget=budget
        account.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("accounts/edit.jinja2",
            account=Account.find_by_id(account_id))

@account_blueprint.route('/delete/<string:account_id>', methods=['GET', 'POST'])
def delete_account(account_id):
    Account.find_by_id(account_id).delete()
    return redirect(url_for('users.user_accounts'))

@account_blueprint.route('/<string:account_id>')
def get_account_page(account_id):
    return render_template('accounts/account.jinja2',
                    account=Account.find_by_id(account_id))

@account_blueprint.route('/')
def index():
    accounts=Account.all()
    return render_template('accounts/account_index.jinja2', accounts=accounts)
