from main import ma

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "customer_name", "customer_mobile", "customer_email", "booking")
    
    booking = ma.List(ma.Nested("BookingSchema", exclude=["customer"]))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)