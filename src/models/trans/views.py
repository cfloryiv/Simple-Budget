from flask import Blueprint, request, render_template, session, redirect, url_for
from models.trans.tran import Trans
from models.control.control import Control
from models.accounts.account import Account
from models.sales.sale import Sale

trans_blueprint=Blueprint('trans', __name__)

@trans_blueprint.route('/new/<string:name>', methods=['GET', 'POST'])
def create_trans(name):
    if request.method=='POST':
        name=request.form['name']
        period=request.form['period']
        amount=float(request.form['amount'])
        trans_date=request.form['trans_date']
        

        trans=Trans(session['email'], name, period, amount, trans_date).save_to_mongo()

        control=Control(period, 'misc')
        control.save_to_mongo()

        account=Account.find_by_name(name)

        sale=Sale.find_by_account_period(name, period)

        sale.name=name
        sale.period=period
        sale.budget=account.budget
        sale.sales+=amount

        sale.save_to_mongo()
        
        return redirect(url_for('.index'))

    control=Control.find_by_id('misc')
    period=control.period
    
    return render_template("trans/new_trans.jinja2", period=period, name=name)

@trans_blueprint.route('/edit/<string:trans_id>', methods=['GET', 'POST'])
def edit_trans(trans_id):
    if request.method=='POST':
        name=request.form['name']
        period=request.form['period']
        amount=float(request.form['amount'])
        trans_date=request.form['trans_date']

        trans=Trans.find_by_id(trans_id)
        trans.name=name
        trans.period=period
        trans.amount=amount
        trans.trans_date=trans_date
        trans.save_to_mongo()

        return redirect(url_for('.list_trans', name=name))

    return render_template("trans/edit.jinja2",
            trans=Trans.find_by_id(trans_id))

@trans_blueprint.route('/delete/<string:trans_id>')
def delete_trans(trans_id):
    trans=Trans.find_by_id(trans_id)
    trans.delete
    return redirect(url_for('.list_trans', name=trans.name))

@trans_blueprint.route('/list/<string:name>')
def list_trans(name):
    trans=Trans.find_by_account(name)
    return render_template('trans/list_trans.jinja2', trans=trans)

@trans_blueprint.route('/<string:trans_id>')
def get_trans_page(trans_id):
    return render_template('trans/trans.jinja2',
                    tran=Trans.find_by_id(trans_id))



