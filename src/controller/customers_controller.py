from flask import Blueprint, request
from schema.customers_schema import customer_schema, customers_schema
from model.customer import Customer
from main import db
from controller.users_controller import make_secure, admin_only
from flask_jwt_extended import jwt_required

customer = Blueprint('customer', __name__, url_prefix='/customers')

@customer.get("/")
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return customers_schema.dump(customers)

@customer.get("/<int:id>")
@jwt_required()
def get_customer(id):
    customer = Customer.query.get(id)

    if not customer:
        return {"message": "Customer does not exist"}
    return customer_schema.dump(customer)

@customer.post("/create")
@jwt_required
def create_customer():
    try:
        customer_fields = customer_schema.load(request.json)
        customer = Customer(**customer_fields)
        mobile = customer.customer_mobile
        if Customer.query.filter_by(customer_mobile=mobile).first():
            return {"message": "A customer with this mobile number already exists!"}
        
        if int(len(mobile)) < 10:
            return {"message": "Please enter a valid mobile number"}
        
        if '@' not in customer.customer_email:
            return {"message": "Please enter a valid email"}
        
        else:
            db.session.add(customer)
            db.session.commit()
            return customer_schema.dump(customer)
    except:
        return {"message": "Looks like some information is missing!"}

@customer.delete('/delete/<int:id>')
@jwt_required
@make_secure("Admin","Manager")
def customer_delete(id):
    customer = Customer.query.filter_by(id=id).first()
    if not customer:
        return {"message": "Customer does not exist"}
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted"}