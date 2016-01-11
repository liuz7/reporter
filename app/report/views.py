#coding:utf-8
from flask import Blueprint, render_template, current_app
import os.path

report = Blueprint('report', __name__, url_prefix='/report')

@report.route('/')
def index():
    report_dir = current_app.config['PPE_REPORT_PATH']
    file_list = []
    os.path.walk(report_dir, step, ('.html', file_list))
    report_list = []
    for file_path in file_list:
        report_list.append(file_path[len(report_dir):-1])
    return render_template('report/index.html', report_list = report_list)



def step((ext, file_list), dirname, names):
    ext = ext.lower()
    for name in names:
        if name.lower().endswith(ext):
            file_list.append(os.path.join(dirname, name))