from flask import Flask
from .database import db
from flask_restful import Api
from flask_login import LoginManager
from .wishes.wishes_resource import WishesListResource, WishesResource
from .users.users_resources import UsersListResource, UsersResource
import os
from config import Config


def create_app():
    app = Flask(__name__)
    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    api = Api(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    api.add_resource(WishesListResource, '/wishes')
    api.add_resource(WishesResource, '/wish/<int:wishes_id>')
    api.add_resource(UsersListResource, '/users')
    api.add_resource(UsersResource, '/user/<int:user_id>')
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    return app
