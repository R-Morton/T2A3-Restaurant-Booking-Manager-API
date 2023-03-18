from main import ma

class CustomerSchema(ma.Schema):
    class Meta:
        #Fields that either get input or displayed
        fields = ("id", "customer_name", "customer_mobile", "customer_email", "booking")
    
    #Displaying connected bookings with the customer data
    booking = ma.List(ma.Nested("BookingSchema", exclude=["customer"]))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)