from flask import Blueprint, request
from schema.customers_schema import customer_schema, customers_schema
from model.customer import Customer
from main import db

customer = Blueprint('customer', __name__, url_prefix='/customers')

@customer.get("/")
def get_customers():
    customers = Customer.query.all()
    return customers_schema.dump(customers)

@customer.get("/<int:id>")
def get_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return {"message": "Customer does not exist"}
    return customer_schema.dump(customer)

@customer.post("/create")
def create_customer():
    customer_fields = customer_schema.load(request.json)

    customer = Customer(**customer_fields)

    db.session.add(customer)
    db.session.commit()

    return customer_schema.dump(customer)