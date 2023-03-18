from flask import Blueprint, request
from schema.bookings_schema import booking_schema, bookings_schema
from model.booking import Booking
from model.customer import Customer
from model.venue import Venue
from model.user import User
from main import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

booking = Blueprint('booking', __name__, url_prefix='/bookings')

# Shows all bookings in the database
@booking.get("/")
@jwt_required()
def get_bookings():
    bookings = Booking.query.all()
    return bookings_schema.dump(bookings)

# Shows specific booking based on the id
@booking.get("/<int:id>")
@jwt_required()
def get_booking(id):
    booking = Booking.query.get(id)
    if not booking:
        return {"message": "Booking does not exist"}
    return booking_schema.dump(booking)

# Creates a booking
@booking.post("/create")
@jwt_required()
def create_booking():
    booking_fields = booking_schema.load(request.json)
    booking = Booking(**booking_fields)

    # Using jwt, this is also checking the role to ensure 'staff' roles cannot book outside their venue.
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if booking.venue_id != user.venue_id:
        if user.roles.name != 'Admin' and user.roles.name != 'Manager':
            return {"message": "You are not authorised to make bookings for other venues"}

    # Checking to make sure the input date is not in the past
    date_str = booking.booking_date
    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
    if date_object < datetime.today().date():
        return {"message": "You cannot choose a date in the past"}

    # Checking the foreign key of the customer id exists
    if not Customer.query.filter_by(id=booking.customer_id).all():
        return {"message": "Customer not found. Please enter a valid customer"}
    
    # Checking the foreign key of the venue id exists
    if not Venue.query.filter_by(id=booking.venue_id).all():
        return {"message": "Venue not found. Please enter a valid venue"}
    
    
    selected_venue = Venue.query.filter_by(id=booking.venue_id).first()
    venue_trading_hours = selected_venue.trading_hours
    open_time = venue_trading_hours[0:4]
    close_time = venue_trading_hours[5:9]
    count = 1

    # checking the time input is valid, being a 4 digit string
    for x in booking.booking_time:
        if count == 3:
            if int(x) > 5:
                return {"message": "Please select a valid time"}
        count += 1

    # Allocating the time slot asked for to a service and ensuring it is within the trading hours of the venue
    if int(booking.booking_time) >= int(open_time) and int(booking.booking_time) <= 1145:
        booking.booking_service = "Breakfast"
    elif int(booking.booking_time) >= 1200 and int(booking.booking_time) <= 1530:
        booking.booking_service = "Lunch"
    elif int(booking.booking_time) >= 1530 and int(booking.booking_time) <= int(close_time):
        booking.booking_service = "Dinner"
    else:
        return {"message": "Please choose a time during opening hours"}
    

    db.session.add(booking)
    db.session.commit()
    return booking_schema.dump(booking)

# Endpoint for deleting bookings by id
@booking.delete('/delete/<int:id>')
@jwt_required()
def booking_delete(id):
    # comparing id in route with id's in the database
    booking = Booking.query.filter_by(id=id).first()
    selected_venue = Venue.query.filter_by(id=booking.venue_id).first()
    if not booking:
        return {"message": "Booking does not exist"}
    db.session.delete(booking)
    db.session.commit()
    db.session.add(selected_venue)
    db.session.commit()

    return {"message": "Booking deleted"}