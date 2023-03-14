from main import ma

class VenueSchema(ma.Schema):
    class Meta:
        fields = ("id", "location", "max_indoor_seating", "max_outdoor_seating", "trading_hours", "user")
    
    user = ma.List(ma.Nested("UserSchema", exclude=["venue"]))


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)