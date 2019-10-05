import datetime

from flask import Flask, escape, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    name = request.args.get('name', 'Estudiante')
    return render_template('index.html', name=name)


@app.route('/solicitar/')
def hello_name(name=None):
    name = request.args.get('name', 'Estudiante')
    return render_template(
        'hello.html',
        name=name,
        date=str(datetime.datetime.now().date())
    )


@app.route('/shift_system/')
def shift_system(name=None):
    name = request.args.get('name', 'Estudiante')
    return render_template('shift_system.html', name=name)
