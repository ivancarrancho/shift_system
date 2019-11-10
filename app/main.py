import datetime

from flask import Flask, escape, request
from flask import render_template
from flask_socketio import SocketIO, emit
from rock import take_shift
from flask_pymongo import PyMongo


app = Flask(__name__)
socketio = SocketIO(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
mongo = PyMongo(app)


@app.route('/')
def index():
    print('********************+')
    # print(mongo)

    # mongo.db.inventory.insert_one({'name': 'ivan'})

    # print(mongo.db.inventory.find({'name': 'ivan'}))

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


@app.route('/ask-shift/<choice>/')
def ask_shift(choice):
    return take_shift(choice=choice)


if __name__ == '__main__':
    socketio.run(app)
