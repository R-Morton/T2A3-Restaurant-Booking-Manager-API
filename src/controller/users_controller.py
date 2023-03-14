from flask import Blueprint, request
import functools
from schema.users_schema import user_schema, users_schema
from schema.roles_schema import role_schema
from model.user import User, Role
from model.venue import Venue
from main import db, login_manager
from flask_login import LoginManager, login_user, login_required, logout_user


user = Blueprint('user', __name__, url_prefix='/users')

def make_secure(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        user = User()
        if user.role_id >= 2:
            return func(*args, **kwargs)
        else:
            return {"message": "You are not authorized"}

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

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
    user = User(** user_fields)
    email = user.email

    if '@' not in user.email:
        return {"message": "Please enter a valid email"}
    
    if not Venue.query.filter_by(id=user.venue_id).all():
        return {"message": "Venue not found. Please enter a valid venue"}

    if User.query.filter_by(email=email).first():
        return {"message": "This email address is already in use. Please login"}
    else:
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

@user.delete('/delete/<int:id>')
def user_delete(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return {"message": "User does not exist"}
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}


