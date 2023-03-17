from main import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    booking_date = db.Column(db.String(), nullable=False)
    booking_time = db.Column(db.String(), nullable=False)
    booking_pax = db.Column(db.Integer(), nullable=False)
    booking_service = db.Column(db.String())
    is_outdoors = db.Column(db.Boolean())
    
    venue_id = db.Column(db.Integer(), db.ForeignKey("venues.id"), nullable=False)
    customer_id = db.Column(db.Integer(), db.ForeignKey("customers.id"), nullable=False)

    venue = db.relationship('Venue', back_populates='booking')
    customer = db.relationship('Customer', back_populates='booking')