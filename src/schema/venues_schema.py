from main import ma

class VenueSchema(ma.Schema):
    class Meta:
        #Fields that either get input or displayed
        fields = ("id", "location", "max_indoor_seating", "max_outdoor_seating", "trading_hours", "user", "current_indoor_seating")
    
    # Displays the users connected to each venue
    user = ma.List(ma.Nested("UserSchema", exclude=["venue"]))


venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)