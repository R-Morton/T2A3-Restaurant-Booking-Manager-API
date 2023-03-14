from flask import Blueprint
from main import db
from model.user import User, Role
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

@db_cmd.cli.command('seed')
def seed_db():
    admin_role = Role(name='Admin')
    manager_role = Role(name='Manager')
    staff_roll = Role(name="Staff")
    db.session.add(admin_role)
    db.session.add(manager_role)
    db.session.add(staff_roll)

    Barangaroo_location = Venue(
        location = "Barangaroo, Sydney",
        max_indoor_seating = 110,
        max_outdoor_seating = 40,
        trading_hours = "0900-2200"
    )
    db.session.add(Barangaroo_location)

    Wahroonga_location = Venue(
        location = "Wahroonga, Sydney",
        max_indoor_seating = 100,
        max_outdoor_seating = 35,
        trading_hours = "0500-2200"
    )
    db.session.add(Wahroonga_location)

    Granville_location = Venue(
        location = "Granville, Sydney",
        max_indoor_seating = 120,
        max_outdoor_seating = 20,
        trading_hours = "0600-2200"
    )
    db.session.add(Granville_location)

    Admin_user = User(
        email = 'admin@admin.com',
        password = 'password',
        name = 'admin',
        role_id = 1)

    db.session.add(Admin_user)
    db.session.commit()
    