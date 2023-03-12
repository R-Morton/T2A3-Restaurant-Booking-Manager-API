from main import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    booking_date = db.Column(db.Date(), nullable=False)
    booking_time = db.Column(db.String(), nullable=False)
    booking_service = db.Column(db.String(), nullable=False)
    is_outdoors = db.Column(db.Boolean())
    
    venue_id = db.Column(db.Integer(), db.ForeignKey("venues.id"), nullable=False)

    venue = db.relationship('Venue', backref='bookings')