from flask import Flask
from flask_restful import Api

from data import db_session
from data import user_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app, catch_all_404s=True)

db_session.global_init("db/mars_explorer.db")


def main():
    api.add_resource(user_resource.UsersListResource, '/api/v2/user')
    api.add_resource(user_resource.UsersResource, '/api/v2/user/<int:user_id>')

    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
