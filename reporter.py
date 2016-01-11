#coding:utf-8
from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_pyfile('instance/config.py')
#app.config.from_envvar('APP_CONFIG_FILE')
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == '__main__':
    app.run()
