from main import db

class Booking(db.Model):
    __tablename__ = "bookings"

    #Primary key
    id = db.Column(db.Integer, primary_key=True)

    booking_date = db.Column(db.String(), nullable=False)
    booking_time = db.Column(db.String(), nullable=False)
    booking_pax = db.Column(db.Integer(), nullable=False)
    booking_service = db.Column(db.String())
    is_outdoors = db.Column(db.Boolean())
    
    #Foreign key for Venue
    venue_id = db.Column(db.Integer(), db.ForeignKey("venues.id"), nullable=False)
    #Foreign key for Customer
    customer_id = db.Column(db.Integer(), db.ForeignKey("customers.id"), nullable=False)

    #Relationships declaration, giving a backref between foreign key tables.
    venue = db.relationship('Venue', back_populates='booking')
    customer = db.relationship('Customer', back_populates='booking')