from flask import Blueprint, request
from schema.venues_schema import venue_schema, venues_schema
from model.venue import Venue
from main import db
from controller.users_controller import make_secure, admin_only
from flask_jwt_extended import jwt_required

venue = Blueprint('venue', __name__, url_prefix='/venues')

@venue.get("/")
@jwt_required()
@make_secure("Admin","Manager")
def get_venues():
    venues = Venue.query.all()
    return venues_schema.dump(venues)

@venue.get("/<int:id>")
@jwt_required()
@make_secure("Admin","Manager")
def get_venue(id):
    venue = Venue.query.get(id)

    if not venue:
        return {"message": "Venue does not exist"}
    return venue_schema.dump(venue)

@venue.post("/register")
@jwt_required()
@make_secure("Admin")
def register_venue():
    venue_fields = venue_schema.load(request.json)

    venue = Venue(**venue_fields)

    location = venue.location
    try:
        if Venue.query.filter_by(location=location).first():
            return {"message": "This venue already exists."}
        else:
            db.session.add(venue)
            db.session.commit()
    except:
        return {"message": "Information is missing, please ensure you have given eveything."}

    return venue_schema.dump(venue)

@venue.delete('/delete/<int:id>')
@jwt_required()
@make_secure("Admin")
def venue_delete(id):
    venue = Venue.query.filter_by(id=id).first()
    if not venue:
        return {"message": "Venue does not exist"}
    db.session.delete(venue)
    db.session.commit()
    return {"message": "Venue deleted"}