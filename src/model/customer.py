from main import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(), nullable=False)
    customer_mobile = db.Column(db.String(), nullable=False, unique=True)
    customer_email = db.Column(db.String(), nullable=False)
    