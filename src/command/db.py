from flask import Blueprint
from main import db
from model.user import User
from model.venue import Venue
from model.booking import Booking
from model.customer import Customer

db_cmd = Blueprint("db", __name__)

@db_cmd.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_cmd.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")