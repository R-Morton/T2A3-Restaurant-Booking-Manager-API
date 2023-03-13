from flask import Blueprint, request
from schema.venues_schema import venue_schema, venues_schema
from model.venue import Venue
from main import db
from controller.users_controller import check_access

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
@check_access(3)
def register_venue():
    venue_fields = venue_schema.load(request.json)

    venue = Venue(**venue_fields)

    db.session.add(venue)
    db.session.commit()

    return venue_schema.dump(venue)