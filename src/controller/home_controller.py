from flask import Blueprint
from flask_jwt_extended import jwt_required

home = Blueprint('home', __name__, url_prefix='/')

# Just a basic home controller, serves no other purpose for this API
@home.get("/")
@jwt_required()
def get_home_page():
    return {"message": "You are at home"}