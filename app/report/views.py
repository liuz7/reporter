#coding:utf-8
from flask import Blueprint, render_template, current_app, request, make_response, redirect, abort, url_for
import os
from RunForm import *
from task import start_command_task, emit_message
from OpenForm import *
from flask_restful import Resource
from app import api
from app import app

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
    full_report_path = get_full_report_path(report_dir, report)
    report_object = None
    try:
        report_object = open(full_report_path)
        content = report_object.read()
    except IOError as e:
        app.logger.error(e)
        return render_template('report/output.html', result = e)
    finally:
        if report_object is not None:
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
        app_name = form.app.data
        script_path = current_app.config['PPE_SCRIPT_PATH']
        result = run_test(script_path, app_name)
    else:
        result = form.app.errors
    emit_message(result)
    app.logger.debug(result)
    return render_template('report/output.html', result = result)

@report.route('/open/', methods=['POST'])
def open_report():
    form = OpenForm()
    if form.validate_on_submit():
        path = form.path.data
        report_dir = current_app.config['PPE_REPORT_PATH']
        full_report_path = get_full_report_path(report_dir, report)
        if os.path.isfile(full_report_path):
            return redirect(url_for('report.show', name = path))
        else:
            result = "can not find %s" % (full_report_path)
    else:
        result = form.path.errors
    app.logger.debug(result)
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

def get_full_report_path(report_dir, report):
    if report.startswith(os.sep):
        full_report_path = report_dir + report
    else:
        full_report_path = os.path.join(report_dir, report)
    return full_report_path

def run_test(script_path, app_name):
    if os.path.isfile(script_path):
        start_command_task([ "python", "-u", script_path, app_name ])
        result = 'Process Started'
    else:
        result = "no file of %s" % (script_path)
    return result

#curl -X POST http://0.0.0.0:5050/report/run/aaa
class RunTest(Resource):
    def post(self, app_name):
        script_path = current_app.config['PPE_SCRIPT_PATH']
        result = run_test(script_path, app_name)
        app.logger.debug(result)
        return {'status': result}, 201

api.add_resource(RunTest, '/report/run/<string:app_name>')

@report.route('/start/')
def start():
    start_command_task([ "python", "-u", '/Users/liugeorge/workspace/reporter/app/report/slow.py' ])
    return render_template('report/output.html')


