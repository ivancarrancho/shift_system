import datetime

from flask import Blueprint
from flask import request
from flask import render_template
# from flask_socketio import SocketIO, emit
from .rock import take_shift
from .extensions import mongo
from bson.objectid import ObjectId


main = Blueprint('main', __name__)

# 5dcf3564e1633863d890a91a  Estudiantes_Nuevos
# 5dcf3565e1633863d890a91b  Estudiantes_Antiguos
# 5dcf3565e1633863d890a91c  Coop_Uniminuto
# 5dcf3565e1633863d890a91d  Postgrados
# 5dcf3565e1633863d890a91e  Pichincha
# 5dcf3565e1633863d890a91f  Reclamos

list_dict = {
    'Estudiantes_Nuevos': '5dcf3564e1633863d890a91a',
    'Estudiantes_Antiguos': '5dcf3565e1633863d890a91b',
    'Coop_Uniminuto': '5dcf3565e1633863d890a91c',
    'Postgrados': '5dcf3565e1633863d890a91d',
    'Pichincha': '5dcf3565e1633863d890a91e',
    'Reclamos': '5dcf3565e1633863d890a91f'
}


def sum_shift(key=None):
    if not key:
        return False

    _id = list_dict[key]
    collections = mongo.db.users

    doc = collections.find_one({'_id': ObjectId(_id)})
    total = int(doc[key]) + 1

    collections.update_one({'_id': ObjectId(_id)}, {'$set': {key: total}})

    return total


@main.route('/empty/')
def empty():
    collections = mongo.db.users
    for key, value in list_dict.items():
        newvalues = {'$set': {key: 0}}
        collections.update_one({'_id': ObjectId(value)}, newvalues)

    return {'ok': True}


@main.route('/')
def index():
    # collections = mongo.db.users

    # estudiantes_nuevos = collections.insert({'Estudiantes_Nuevos': 0})
    # estudiantes_antiguos = collections.insert({'Estudiantes_Antiguos': 0})
    # coop_uniminuto = collections.insert({'Coop_Uniminuto': 0})
    # postgrados = collections.insert({'Postgrados': 0})
    # pichincha = collections.insert({'Pichincha': 0})
    # reclamos = collections.insert({'Reclamos': 0})

    # doc = collections.find_one({'_id': ObjectId('5dcf3564e1633863d890a91a')})

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
    collections = mongo.db.users
    name = request.args.get('name', 'Estudiante')
    date = request.args.get('date', '--')
    shift = request.args.get('shift')

    actual_shift = sum_shift(key=shift)

    return render_template(
        'shift_system.html',
        name=name.replace('_', ' '),
        date=date,
        shift=shift,
        actual_shift=actual_shift if actual_shift else '-',
        Estudiantes_Nuevos=collections.find_one(
            {'_id': ObjectId(list_dict['Estudiantes_Nuevos'])}
        ).get('Estudiantes_Nuevos'),
        Estudiantes_Antiguos=collections.find_one(
            {'_id': ObjectId(list_dict['Estudiantes_Antiguos'])}
        ).get('Estudiantes_Antiguos'),
        Coop_Uniminuto=collections.find_one(
            {'_id': ObjectId(list_dict['Coop_Uniminuto'])}
        ).get('Coop_Uniminuto'),
        Postgrados=collections.find_one(
            {'_id': ObjectId(list_dict['Postgrados'])}
        ).get('Postgrados'),
        Pichincha=collections.find_one(
            {'_id': ObjectId(list_dict['Pichincha'])}
        ).get('Pichincha'),
        Reclamos=collections.find_one(
            {'_id': ObjectId(list_dict['Reclamos'])}
        ).get('Reclamos'),
    )


@main.route('/ask-shift/<choice>/')
def ask_shift(choice):
    return take_shift(choice=choice)


# if __name__ == '__main__':
#     socketio.run(app)
