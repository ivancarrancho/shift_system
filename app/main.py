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
    'Reclamos': '5dcf3565e1633863d890a91f',
    'Estudiantes_Nuevos_shift': '5dd1f0133e0b854b1854952f',
    'Estudiantes_Antiguos_shift': '5dd1f0133e0b854b18549530',
    'Coop_Uniminuto_shift': '5dd1f0133e0b854b18549531',
    'Postgrados_shift': '5dd1f0133e0b854b18549532',
    'Pichincha_shift': '5dd1f0133e0b854b18549533',
    'Reclamos_shift': '5dd1f0133e0b854b18549534',
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

    return render_template('admin_module.html', empty=True)


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
    s_shift = sum_shift(key=shift)
    return render_template(
        'hello.html',
        url=name.replace(' ', '_'),
        name=name,
        date=str(datetime.datetime.now().date()),
        shift=shift,
        s_shift=s_shift
    )


@main.route('/shift_system/')
def shift_system(name=None):
    collections = mongo.db.users
    name = request.args.get('name', 'Estudiante')
    date = request.args.get('date', '--')
    shift = request.args.get('shift')
    s_shift = request.args.get('s_shift')

    return render_template(
        'shift_system.html',
        name=name.replace('_', ' '),
        date=date,
        shift=shift,
        actual_shift=shift,
        s_shift=s_shift,
        Estudiantes_Nuevos=collections.find_one(
            {'_id': ObjectId(list_dict['Estudiantes_Nuevos_shift'])}
        ).get('Estudiantes_Nuevos_shift'),
        Estudiantes_Antiguos=collections.find_one(
            {'_id': ObjectId(list_dict['Estudiantes_Antiguos_shift'])}
        ).get('Estudiantes_Antiguos_shift'),
        Coop_Uniminuto=collections.find_one(
            {'_id': ObjectId(list_dict['Coop_Uniminuto_shift'])}
        ).get('Coop_Uniminuto_shift'),
        Postgrados=collections.find_one(
            {'_id': ObjectId(list_dict['Postgrados_shift'])}
        ).get('Postgrados_shift'),
        Pichincha=collections.find_one(
            {'_id': ObjectId(list_dict['Pichincha_shift'])}
        ).get('Pichincha_shift'),
        Reclamos=collections.find_one(
            {'_id': ObjectId(list_dict['Reclamos_shift'])}
        ).get('Reclamos_shift'),
    )


@main.route('/ask-shift/<choice>/')
def ask_shift(choice):
    sum_shift(key=choice)
    # collections = mongo.db.users

    # estudiantes_nuevos = collections.insert({'Estudiantes_Nuevos_shift': 0})
    # estudiantes_antiguos = collections.insert({'Estudiantes_Antiguos_shift': 0})
    # coop_uniminuto = collections.insert({'Coop_Uniminuto_shift': 0})
    # postgrados = collections.insert({'Postgrados_shift': 0})
    # pichincha = collections.insert({'Pichincha_shift': 0})
    # reclamos = collections.insert({'Reclamos_shift': 0})

    return render_template('change_shift.html', choice=choice)


@main.route('/admin/')
def admin_module():
    return render_template('admin_module.html')


# if __name__ == '__main__':
#     socketio.run(app)
