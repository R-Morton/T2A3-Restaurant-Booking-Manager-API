from main import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    manager = db.Column(db.Boolean())

    venue_id = db.Column(
        db.Integer(), db.ForeignKey("venues.id"), nullable=False
        )

    venue = db.relationship('Venue', backref='user')
