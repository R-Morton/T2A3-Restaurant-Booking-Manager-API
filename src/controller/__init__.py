from controller.home_controller import home
from controller.users_controller import user
from controller.venue_controller import venue
from controller.customers_controller import customer
from controller.bookings_controller import booking

registerable_controllers = [
    home,
    user,
    venue,
    customer,
    booking,
]