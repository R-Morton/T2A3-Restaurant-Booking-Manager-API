from flask import Blueprint, request
from schema.venues_schema import venue_schema, venues_schema
from model.venue import Venue
from main import db
from controller.users_controller import make_secure, admin_only
from flask_jwt_extended import jwt_required

venue = Blueprint('venue', __name__, url_prefix='/venues')

# Endpoint showing all venues
@venue.get("/")
@jwt_required()
@make_secure("Admin","Manager")
def get_venues():
    venues = Venue.query.all()
    return venues_schema.dump(venues)

# Endpoint showing venue by id
@venue.get("/<int:id>")
@jwt_required()
@make_secure("Admin","Manager")
def get_venue(id):
    venue = Venue.query.get(id)

    if not venue:
        return {"message": "Venue does not exist"}
    return venue_schema.dump(venue)

#Endpoint for registering new venues
@venue.post("/register")
@jwt_required()
@make_secure("Admin")
def register_venue():
    try:
        venue_fields = venue_schema.load(request.json)
        venue = Venue(**venue_fields)
        location = venue.location

        #Error checking to ensure trading hours field format is correct
        if len(venue.trading_hours) != 9:
            return {"message": "Please enter a valid trading hours time. XXXX-XXXX"}

        if Venue.query.filter_by(location=location).first():
            return {"message": "This venue already exists."}
        
        #Error checking to ensure trading hours field format is correct
        string_numbers = ['0','1','2','3','4','5','6','7','8','9','-']
        count = 0
        for x in venue.trading_hours:
            if count <= 3 or count >= 5:
                if x not in string_numbers[0:9]:
                    return {"message": "Please enter a valid trading hours time. XXXX-XXXX"}
            if count == 4:
                if x not in string_numbers[10]:
                    return {"message": "Please enter a valid trading hours time. XXXX-XXXX"}
            count += 1
        
        db.session.add(venue)
        db.session.commit()
        return venue_schema.dump(venue)
    except:
        return {"message": "Looks like some information is missing"}

#End point to delete venue using id.
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