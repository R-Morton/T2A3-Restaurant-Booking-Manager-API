from flask import Blueprint, request
from schema.bookings_schema import booking_schema, bookings_schema
from model.booking import Booking
from main import db

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

    db.session.add(booking)
    db.session.commit()

    return booking_schema.dump(booking)