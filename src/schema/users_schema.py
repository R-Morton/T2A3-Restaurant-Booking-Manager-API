from main import ma

class UserSchema(ma.Schema):
    class Meta:
        #Fields that either get input or displayed
        fields = ("id", "email", "password", "name", "venue_id", "venue", "roles", "role_id")
        #These are excluded from serialized results
        load_only = ["venue_id", "role_id"]
    
    #These get displayed with the User data
    venue = ma.Nested("VenueSchema", exclude=["user"])
    roles = ma.Nested("RoleSchema")

user_schema = UserSchema()
users_schema = UserSchema(many=True)