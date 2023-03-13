from main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "name", "venue_id", "venue")
        load_only = ["venue_id"]
    
    venue = ma.Nested("VenueSchema", exclude=["user"])

user_schema = UserSchema()
users_schema = UserSchema(many=True)