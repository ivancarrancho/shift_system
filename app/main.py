import datetime

from flask import Blueprint
from flask import request
from flask import render_template
# from flask_socketio import SocketIO, emit
from .rock import take_shift
from .extensions import mongo


main = Blueprint('main', __name__)


@main.route('/')
def index():
    # print(mongo)
    # client = pymongo.MongoClient("")
    # db = client.test
    # mongo.db.inventory.insert_one({'name': 'ivan'})
    collections = mongo.db.users
    collections.insert({'Hola': 'bitchis'})

    name = request.args.get('name', 'Estudiante')
    return render_template('index.html', name=name)


@main.route('/solicitar/')
def hello_name(name=None):
    name = request.args.get('name', 'Estudiante')
    shift = request.args.get('shift')
    return render_template(
        'hello.html',
        url=name.replace(' ', '_'),
        name=name,
        date=str(datetime.datetime.now().date()),
        shift=shift
    )


@main.route('/shift_system/')
def shift_system(name=None):
    name = request.args.get('name', 'Estudiante')
    date = request.args.get('date', '--')
    return render_template(
        'shift_system.html',
        name=name.replace('_', ' '),
        date=date
    )


@main.route('/ask-shift/<choice>/')
def ask_shift(choice):
    return take_shift(choice=choice)


# if __name__ == '__main__':
#     socketio.run(app)
