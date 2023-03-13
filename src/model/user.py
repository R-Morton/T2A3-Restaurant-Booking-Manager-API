from main import db
from flask_login import LoginManager, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    security_level = db.Column(db.Integer())

    venue_id = db.Column(
        db.Integer(), db.ForeignKey("venues.id"), nullable=False
        )

    venue = db.relationship('Venue', backref='user')

    def allowed(self, security_level):
        return self.security_level >= security_level
