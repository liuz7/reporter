from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object('config.default')
app.config.from_pyfile('instance/config.py')
#app.config.from_envvar('APP_CONFIG_FILE')
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

from app.report.views import report as report_module

app.register_blueprint(report_module)