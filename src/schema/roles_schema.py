from main import ma

class RoleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
    

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)