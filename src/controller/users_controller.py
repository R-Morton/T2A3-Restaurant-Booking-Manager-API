from flask import Blueprint, request
from schema.users_schema import user_schema, users_schema
from model.user import User
from main import db

user = Blueprint('user', __name__, url_prefix='/users')

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

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user)