from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
import eventlet
from flask.ext.socketio import SocketIO
from flask_restful import Api

eventlet.monkey_patch()

app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_pyfile('instance/config.py')
#app.config.from_envvar('APP_CONFIG_FILE')

bootstrap = Bootstrap(app)
socketio = SocketIO(app)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

from app.report.views import report as report_module

app.register_blueprint(report_module)
