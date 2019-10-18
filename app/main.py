import datetime

from flask import Flask, escape, request
from flask import render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    name = request.args.get('name', 'Estudiante')
    return render_template('index.html', name=name)


@app.route('/solicitar/')
def hello_name(name=None):
    name = request.args.get('name', 'Estudiante')
    return render_template(
        'hello.html',
        url=name.replace(' ', '_'),
        name=name,
        date=str(datetime.datetime.now().date())
    )


@app.route('/shift_system/')
def shift_system(name=None):
    name = request.args.get('name', 'Estudiante')
    date = request.args.get('date', '--')
    return render_template(
        'shift_system.html',
        name=name.replace('_', ' '),
        date=date
    )

if __name__ == '__main__':
    socketio.run(app)