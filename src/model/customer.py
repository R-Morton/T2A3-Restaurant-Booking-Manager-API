from main import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(), nullable=False)
    customer_mobile = db.Column(db.String(), nullable=False)
    customer_email = db.Column(db.String(), nullable=False)
    
    booking_id = db.Column(db.Integer(), db.ForeignKey("bookings.id"), nullable=False)

    booking = db.relationship('Booking', backref='customers')