from main import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "name", "venue_id", "venue", "roles", "role_id")
        load_only = ["venue_id", "role_id"]
    
    venue = ma.Nested("VenueSchema", exclude=["user"])
    roles = ma.Nested("RoleSchema")

user_schema = UserSchema()
users_schema = UserSchema(many=True)