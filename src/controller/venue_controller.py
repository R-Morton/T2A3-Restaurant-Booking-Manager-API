from flask import Blueprint, request
from schema.venues_schema import venue_schema, venues_schema
from model.venue import Venue
from main import db

venue = Blueprint('venue', __name__, url_prefix='/venues')

@venue.get("/")
def get_venues():
    venues = Venue.query.all()
    return venues_schema.dump(venues)

@venue.get("/<int:id>")
def get_venue(id):
    venue = Venue.query.get(id)

    if not venue:
        return {"message": "Venue does not exist"}
    return venue_schema.dump(venue)

@venue.post("/register")
def register_venue():
    venue_fields = venue_schema.load(request.json)

    venue = Venue(**venue_fields)

    location = venue.location

    if Venue.query.filter_by(location=location).first():
        return {"message": "This venue already exists."}
    else:
        db.session.add(venue)
        db.session.commit()

    return venue_schema.dump(venue)