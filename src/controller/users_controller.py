from flask import Blueprint, request, jsonify
import functools
from schema.users_schema import user_schema, users_schema
from schema.roles_schema import role_schema
from model.user import User, Role
from model.venue import Venue
from main import db
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, JWTManager

user = Blueprint('user', __name__, url_prefix='/users')

# A decorator function with a parameter that uses JWT and checks the role of the logged in user.
# Use decorator plus the role as an argument to only allow access to users with these roles.
def make_secure(*access_level):
    def decorator(func):
        @functools.wraps(func)
        def secure_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            for level in access_level:
                if user.roles.name == level:
                    return func(*args, **kwargs)
            return {"message": "You are not authorized to do this"}
        return secure_function
    return decorator

# Used to check admin status but as a function, not decorator.
def admin_only():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.roles.name == "Admin":
        return True
    else:
        return False

# Endpoint getting all users
@user.get("/")
@jwt_required()
@make_secure("Admin")
def get_users():
    users = User.query.all()
    return users_schema.dump(users)

# Endpoint getting user by id
@user.get("/<int:id>")
@jwt_required()
@make_secure("Admin")
def get_user(id):
    user = User.query.get(id)

    if not user:
        return {"message": "User does not exist"}
    return user_schema.dump(user)

# Endpoint for registering new users
@user.post("/register")
@jwt_required()
@make_secure("Admin","Manager")
def register_user():
    user_fields = user_schema.load(request.json)
    user = User(** user_fields)
    email = user.email

    # Stops non admins from creating an admin account
    if user.role_id == 1:
        if admin_only() == False:
            return {"message": "Only admins can create an admin account"}
    
    #Basic error checking to ensure an '@' is in the email field
    if '@' not in user.email:
        return {"message": "Please enter a valid email"}
    
    # Checking the foreign key of the venue id exists
    if not Venue.query.filter_by(id=user.venue_id).all():
        return {"message": "Venue not found. Please enter a valid venue"}

    # Error checking for duplicate user
    if User.query.filter_by(email=email).first():
        return {"message": "This email address is already in use. Please login"}
    else:
        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user)

# Endpoint that generates a JWT key if login is successful.
@user.post('/login')
def user_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return {"message": "user not found"}
    else:
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"user":user.email, "token": access_token })


# Endpoint to delete users by id.
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


