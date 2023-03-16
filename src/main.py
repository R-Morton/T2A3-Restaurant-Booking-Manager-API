from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    jwt = JWTManager(app)

    app.config.from_object("config.app_config")
    app.config['SECRET_KEY'] = 'supersecretbruh'
    app.config["JWT_SECRET_KEY"] = "Backend best end"

    db.init_app(app)
    ma.init_app(app)
    jwt = JWTManager(app)

    from command.db import db_cmd
    app.register_blueprint(db_cmd)

    from controller import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
