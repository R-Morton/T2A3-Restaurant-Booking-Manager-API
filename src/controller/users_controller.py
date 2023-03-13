from flask import Blueprint, request
from schema.users_schema import user_schema, users_schema
from model.user import User, Role
from main import db, login_manager
from flask_login import LoginManager, login_user, login_required, logout_user


user = Blueprint('user', __name__, url_prefix='/users')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return {"message": "you must be logged in"}

@user.get("/")
def get_users():
    users = User.query.all()
    return users_schema.dump(users)

@user.get("/<int:id>")
def get_user(id):
    user = User.query.get(id)

    if not user:
        return {"message": "User does not exist"}
    return user_schema.dump(user)

@user.post("/register")
def register_user():
    user_fields = user_schema.load(request.json)

    user = User(**user_fields)
    user.roles = ["Admin"]

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user)

@user.route('/login')
def user_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return {"message": "user not found"}
    else:
        login_user(user)
        return {"message": "you are logged in"}

@user.route('/logout')
@login_required
def user_logout():
    logout_user()
    return {"message": "You are now logged out"}


