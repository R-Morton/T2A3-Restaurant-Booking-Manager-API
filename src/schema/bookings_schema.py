from main import ma

class BookingSchema(ma.Schema):
    class Meta:
        #Fields that either get input or displayed
        fields = ("id", "booking_date", "booking_time", "booking_service", "is_outdoors", "venue_id", "venue", "customer_id", "customer", "booking_pax")
        #These are excluded from serialized results
        load_only = ["venue_id", "customer_id"]
    
    #These display the connecting venue and customer of the booking
    venue = ma.Nested("VenueSchema", exclude=["user"])
    customer = ma.Nested("CustomerSchema", exclude=["booking"])

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)