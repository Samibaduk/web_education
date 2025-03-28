from . import db_session
from .users import User
from flask_restful import abort, Resource
from .reqparse_user import parser

from flask import jsonify

from werkzeug.security import generate_password_hash


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")

def set_password(password):
    generate_password_hash(password)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'rest': users.to_dict(
            only=('name', 'surname', 'age', 'adress', 'email', 'position'
                                                               'speciality', 'hashed_password'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'rest': [item.to_dict(
            only=('name', 'surname', 'age', 'address', 'email', 'position',
                                                               'speciality', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            address=args['address'],
            email=args['email'],
            position=args['position'],
            speciality=args['speciality'],
            hashed_password=set_password(args['hashed_password']))
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})
