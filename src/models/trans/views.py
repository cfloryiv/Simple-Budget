from flask import Blueprint, request, render_template, session, redirect, url_for
from models.trans.tran import Trans

trans_blueprint=Blueprint('trans', __name__)

@trans_blueprint.route('/new', methods=['GET', 'POST'])
def create_trans():
    if request.method=='POST':
        name=request.form['name']
        period=request.form['period']
        amount=float(request.form['amount'])
        trans_date=request.form['trans_date']
        

        trans=Trans(session['email'], name, period, amount, trans_date).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("trans/new_trans.jinja2")

@trans_blueprint.route('/edit/<string:trans_id>', methods=['GET', 'POST'])
def edit_trans(trans_id):
    if request.method=='POST':
        name=request.form['name']
        period=request.form['period']
        amount=float(request.form['amount'])
        trans_date=request.form['trans_date']

        trans=Account.find_by_id(trans_id)
        trans.name=name
        trans.period=period
        trans.amount=amount
        trans.trans_date=trans_date
        trans.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("trans/edit.jinja2",
            trans=Trans.find_by_id(trans_id))

@trans_blueprint.route('/delete/<string:trans_id>', methods=['GET', 'POST'])
def delete_trans(trans_id):
    Trans.find_by_id(trans_id).delete()
    return redirect(url_for('users.user_trans'))

@trans_blueprint.route('/<string:trans_id>')
def get_trans_page(trans_id):
    return render_template('trans/trans.jinja2',
                    trans=Trans.find_by_id(trans_id))

@trans_blueprint.route('/')
def index():
    trans=Trans.all()
    return render_template('trans/trans_index.jinja2', trans=trans)

