from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

#Initializes a flask instance, connecting all config data
def create_app():
    app = Flask(__name__)

    app.config.from_object("config.app_config")
    app.config["JWT_SECRET_KEY"] = "Backend best end"

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from command.db import db_cmd
    app.register_blueprint(db_cmd)

    from controller import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
