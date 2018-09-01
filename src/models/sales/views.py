from flask import Blueprint, request, render_template, session, redirect, url_for
from models.sales.sale import Sale

sales_blueprint=Blueprint('sales', __name__)



@sales_blueprint.route('/month_report')
def month_report():
    sales=Sale.find_by_period()
    return render_template('sales/month_report.jinja2',
                    sales=sales)

@sales_blueprint.route('/year_report')
def year_report():
    sales=Sale.all()
    return render_template('sales/year_report.jinja2', sales=sales)

@sales_blueprint.route('/periods_report')
def periods_report():
    sales=Sale.find_by_periods()
    return render_template('sales/periods_report.jinja2', sales=sales)
