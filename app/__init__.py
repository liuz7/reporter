from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
import eventlet
from flask.ext.socketio import SocketIO
from flask_restful import Api
import logging
from logging.handlers import RotatingFileHandler
from flask.ext.compress import Compress

eventlet.monkey_patch()

app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_pyfile('instance/config.py', silent=True)
#app.config.from_envvar('APP_CONFIG_FILE')

Compress(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)
api = Api(app)

handler = RotatingFileHandler(
    app.config['LOGGING_LOCATION'],
    maxBytes=1024 * 1024 * 10,
    backupCount=2
    )
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app_list = app.config['APP_LIST']
report_dir = app.config['PPE_REPORT_PATH']
script_path = app.config['PPE_SCRIPT_PATH']

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

from app.report.views import report as report_module

app.register_blueprint(report_module)
