#coding:utf-8
from flask import Blueprint, render_template, current_app, request, make_response, redirect, abort, url_for
import os
from RunForm import *
from task import start_command_task, emit_message
from OpenForm import *

report = Blueprint('report', __name__, url_prefix='/report')

@report.route('/')
def index():
    run_form = RunForm()
    open_form = OpenForm()
    report_dir = current_app.config['PPE_REPORT_PATH']
    html_report_list = get_file_list_by_ext(report_dir, '.html')
    report_list = list(set(map(lambda x: os.path.dirname(x), html_report_list)))
    debug_report_list = get_file_list_by_ext(report_dir, '.debug')
    return render_template('report/index.html', report_list = report_list, debug_report_list = debug_report_list, run_form = run_form, open_form = open_form)

@report.route('/show/')
def show():
    report_dir = current_app.config['PPE_REPORT_PATH']
    report = request.args.get('name', '')
    if report.startswith(os.sep):
        full_report_path = report_dir + report
    else:
        full_report_path = os.path.join(report_dir, report)
    report_object = open(full_report_path)
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

@report.route('/open/', methods=['POST'])
def open_report():
    form = OpenForm()
    if form.validate_on_submit():
        path = form.path.data
        report_dir = current_app.config['PPE_REPORT_PATH']
        if path.startswith(os.sep):
            full_report_path = report_dir + path
        else:
            full_report_path = os.path.join(report_dir, path)
        if os.path.isfile(full_report_path):
            return redirect(url_for('report.show', name = path))
        else:
            result = "can not find %s" % (full_report_path)
    else:
        result = form.path.errors
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


