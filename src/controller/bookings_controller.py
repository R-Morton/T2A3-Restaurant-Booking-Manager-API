from flask import Blueprint, request
from schema.bookings_schema import booking_schema, bookings_schema
from model.booking import Booking
from model.customer import Customer
from model.venue import Venue
from main import db
from datetime import datetime

booking = Blueprint('booking', __name__, url_prefix='/bookings')

@booking.get("/")
def get_bookings():
    bookings = Booking.query.all()
    return bookings_schema.dump(bookings)

@booking.get("/<int:id>")
def get_booking(id):
    booking = Booking.query.get(id)

    if not booking:
        return {"message": "Booking does not exist"}
    return booking_schema.dump(booking)

@booking.post("/create")
def create_booking():
    booking_fields = booking_schema.load(request.json)
    booking = Booking(**booking_fields)

    date_str = booking.booking_date
    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
    if date_object < datetime.today().date():
        return {"message": "You cannot choose a date in the past"}

    if not Customer.query.filter_by(id=booking.customer_id).all():
        return {"message": "Customer not found. Please enter a valid customer"}

    if not Venue.query.filter_by(id=booking.venue_id).all():
        return {"message": "Venue not found. Please enter a valid venue"}
    
    selected_venue = Venue.query.filter_by(id=booking.venue_id).first()
    venue_trading_hours = selected_venue.trading_hours
    open_time = venue_trading_hours[0:4]
    close_time = venue_trading_hours[5:9]
    count = 1
    for x in booking.booking_time:
        if count == 3:
            if int(x) > 5:
                return {"message": "Please select a valid time"}
        count += 1

    if int(booking.booking_time) >= int(open_time) or int(booking.booking_time) <= 1145:
        booking.booking_service = "Breakfast"
    elif int(booking.booking_time) >= 1200 or int(booking.booking_time) <= 1530:
        booking.booking_service = "Lunch"
    elif int(booking.booking_time) >= 1530 or int(booking.booking_time) <= int(close_time):
        booking.booking_service = "Dinner"
    else:
        return {"message": "Please choose a time during opening hours"}
    db.session.add(booking)
    db.session.commit()

    return booking_schema.dump(booking)

@booking.delete('/delete/<int:id>')
def booking_delete(id):
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return {"message": "Booking does not exist"}
    db.session.delete(booking)
    db.session.commit()
    return {"message": "Booking deleted"}