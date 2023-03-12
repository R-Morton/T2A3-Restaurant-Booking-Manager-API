from main import ma

class BookingSchema(ma.Schema):
    class Meta:
        fields = ("id", "booking_date", "booking_time", "booking_service", "is_outdoors", "venue_id", "venue", "customer_id", "customer")
        load_only = ["venue_id", "customer_id"]
    
    venue = ma.Nested("VenueSchema", exclude=["user"])
    customer = ma.Nested("CustomerSchema", exclude=["booking"])

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)