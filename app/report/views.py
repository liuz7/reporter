#coding:utf-8
from flask import Blueprint, render_template, current_app, request, make_response, redirect, abort
import os
from RunForm import *
from task import start_command_task, emit_message

report = Blueprint('report', __name__, url_prefix='/report')

@report.route('/')
def index():
    form = RunForm()
    report_dir = current_app.config['PPE_REPORT_PATH']
    html_report_list = get_file_list_by_ext(report_dir, '.html')
    report_list = list(set(map(lambda x: os.path.dirname(x), html_report_list)))
    debug_report_list = get_file_list_by_ext(report_dir, '.debug')
    return render_template('report/index.html', report_list = report_list, debug_report_list = debug_report_list, form = form)

@report.route('/show/')
def show():
    report_dir = current_app.config['PPE_REPORT_PATH']
    report = request.args.get('name', '')
    report_object = open(report_dir + report)
    try:
        content = report_object.read()
    finally:
        report_object.close()
    response = make_response(content)
    if str(report).endswith('.debug'):
        response.mimetype = "text/plain;charset=utf-8"
    return response

@report.route('/show/<log>')
def show_log(log):
    if str(log).startswith('log.html'):
        return redirect(str(request.referrer).replace('report.html', 'log.html'))
    else:
        return abort(404)

@report.route('/run/', methods=['POST'])
def run():
    form = RunForm()
    if form.validate_on_submit():
        app = form.app.data
        script_path = current_app.config['PPE_SCRIPT_PATH']
        if os.path.isfile(script_path):
            start_command_task([ "python", "-u", script_path, app ])
            result = 'Process Started'
        else:
            result = "no file of %s" % (script_path)
    else:
        result = form.app.errors
    emit_message(result)
    return render_template('report/output.html', result = result)

def step((ext, file_list), dirname, names):
    ext = ext.lower()
    for name in names:
        if name.lower().endswith(ext):
            file_list.append(os.path.join(dirname, name))

def get_file_list_by_ext(top_dir, ext):
    file_list = []
    os.path.walk(top_dir, step, (ext, file_list))
    result_list = list(set(map(lambda x: x[len(top_dir):], file_list)))
    return result_list

@report.route('/start/')
def start():
    start_command_task([ "python", "-u", '/Users/liugeorge/workspace/reporter/app/report/slow.py' ])
    return render_template('report/output.html')


