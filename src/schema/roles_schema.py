from main import ma

class RoleSchema(ma.Schema):
    class Meta:
        #Fields that either get input or displayed
        fields = ("id", "name")
    

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)