from main import db
from flask_login import LoginManager, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    #Foreign key
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())

    #Foreign key connecting Role table
    role_id = db.Column(
        db.Integer(), db.ForeignKey("roles.id"))

    #Foreign key connecting Venue table
    venue_id = db.Column(
        db.Integer(), db.ForeignKey("venues.id"))
    
    #Relationships declaration, giving a backref between foreign key tables.
    venue = db.relationship('Venue', backref='user')
    roles = db.relationship('Role', backref='user')

#Table for user roles
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

