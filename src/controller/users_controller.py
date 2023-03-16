from flask import Blueprint, request, jsonify
import functools
from schema.users_schema import user_schema, users_schema
from schema.roles_schema import role_schema
from model.user import User, Role
from model.venue import Venue
from main import db, login_manager
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, JWTManager

user = Blueprint('user', __name__, url_prefix='/users')

def make_secure(*access_level):
    def decorator(func):
        @functools.wraps(func)
        def secure_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            for level in access_level:
                if user.roles.name == level:
                    return func(*args, **kwargs)
            return {"message": "You are not authorized"}
        return secure_function
    return decorator

def admin_only():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.roles.name == "Admin":
        return True
    else:
        return False


@user.get("/")
@jwt_required()
@make_secure("Admin")
def get_users():
    users = User.query.all()
    return users_schema.dump(users)

@user.get("/<int:id>")
@jwt_required()
@make_secure("Admin")
def get_user(id):
    user = User.query.get(id)

    if not user:
        return {"message": "User does not exist"}
    return user_schema.dump(user)

@user.post("/register")
@jwt_required()
@make_secure("Admin","Manager")
def register_user():
    user_fields = user_schema.load(request.json)
    user = User(** user_fields)
    email = user.email

    if user.role_id == 1:
        if admin_only() == False:
            return {"message": "Only admins can create an admin account"}
        
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

@user.post('/login')
def user_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return {"message": "user not found"}
    else:
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token)

@user.route('/logout')
def user_logout():
    return {"message": "You are now logged out"}

@user.delete('/delete/<int:id>')
@jwt_required()
@make_secure("Admin","Manager")
def user_delete(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return {"message": "User does not exist"}
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}


