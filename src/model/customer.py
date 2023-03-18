from main import db

class Customer(db.Model):
    __tablename__ = "customers"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(), nullable=False)
    customer_mobile = db.Column(db.String(), nullable=False, unique=True)
    customer_email = db.Column(db.String(), nullable=False)

    #Expanding relationship for cascade delete setting
    booking = db.relationship('Booking', cascade='all, delete')