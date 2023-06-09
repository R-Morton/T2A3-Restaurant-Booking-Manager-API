from main import db

class Venue(db.Model):
    __tablename__ = "venues"

    #Primary key
    id = db.Column(db.Integer, primary_key=True)

    location = db.Column(db.String(), nullable=False, unique=True)
    max_indoor_seating = db.Column(db.Integer(), nullable=False)
    max_outdoor_seating = db.Column(db.Integer(), nullable=False)
    trading_hours = db.Column(db.String(), nullable=False)

    #Expanding relationship for cascade delete setting
    booking = db.relationship('Booking', cascade='all, delete')

