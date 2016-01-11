#coding:utf-8
from flask import Blueprint, render_template

report = Blueprint('report', __name__, url_prefix='/report')

@report.route('/')
def index():
    return render_template('report/index.html')
