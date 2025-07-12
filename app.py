from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
from werkzeug.exceptions import BadRequest
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app) 



app.config['SECRET_KEY'] = "3d6f45a5fc12445dbac2f59c3b6c7cb1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://project:1234@localhost:5432/rentalcar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'   
def check_email(email):   
  
    if(re.search(regex,email)):   
        return True  
    else:   
        return False 
   
class Customer(db.Model):
    __tablename__ = "customer"
    dl_number = db.Column(db.String(30), primary_key = True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(50), nullable=False)  
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    Reservations =  db.relationship('BookingDetails', backref="customer")

    def __repr__(self):
        return f"Customer('{self.dl_number}')"


class Car_Category(db.Model):
    __tablename__ = "car_category"
    category_name = db.Column(db.String(25), primary_key = True, nullable=False)
    no_of_person = db.Column(db.Integer, nullable=False)
    cars = db.relationship('Car', backref="car_category")  
    cost_per_day = db.Column(db.Float, nullable=False)
    late_fee_per_hour = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"CAR_CATEGORY('{self.category_name}')"


class LocationDetails(db.Model):
    __tablename__ = "location_details"
    location_id = db.Column(db.Integer, primary_key = True, nullable=False)
    location_name = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(30), nullable=False)
    cars = db.relationship('Car', backref="location_details")
    Reservations =  db.relationship('BookingDetails', backref="location_details")
    city = db.Column(db.String(20), nullable=False)
    state_name = db.Column(db.String(20), nullable=False)
    post_code = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"LocationDetails('{self.location_id}')"


class Car(db.Model):
    __tablename__ = "car"
    registration_number = db.Column(db.Integer, primary_key = True, nullable=False)
    availability_flag = db.Column(db.Boolean, nullable=False)
    model_name = db.Column(db.String(25), nullable=False)  
    loc_id = db.Column(db.ForeignKey("location_details.location_id"), nullable=False)
    car_categories = db.Column(db.ForeignKey("car_category.category_name"), nullable=False)
    maker = db.Column(db.String(25), nullable=False)
    kilometers = db.Column(db.Integer, nullable=False)
    Reservations =  db.relationship('BookingDetails', backref="car")

    def __repr__(self):
        return f"CAR('{self.registration_number}')"
    
class RentalCarInsurance(db.Model):
    __tablename__ = "rental_car_insurance"
    insurance_code = db.Column(db.Integer, primary_key = True, nullable=False)
    insurance_name = db.Column(db.String(50), nullable=False, unique=True)
    coverage_type = db.Column(db.String(100), nullable=False)
    cost_per_day = db.Column(db.Float, nullable=False)
    Reservations =  db.relationship('BookingDetails', backref="rental_car_insurance")
    def __repr__(self):
        return f"RentalCarInsurance('{self.insurance_code}')"

class BookingDetails(db.Model):
    __tablename__ = "booking_details"
    booking_id = db.Column(db.Integer, primary_key = True, nullable=False)
    from_dt_time = db.Column(db.DateTime, nullable=False)
    ret_dt_time = db.Column(db.DateTime, nullable=False)
    reservation_status = db.Column(db.Boolean, nullable=False)
    pickup_loc = db.Column(db.ForeignKey("location_details.location_id"), nullable=False)
    reg_num = db.Column(db.ForeignKey("car.registration_number"), nullable=False)
    dl_num = db.Column(db.ForeignKey("customer.dl_number"), nullable=False)
    ins_code = db.Column(db.ForeignKey("rental_car_insurance.insurance_code"), nullable=False)
    bills = db.relationship("BillingDetails", backref="booking_details")

    def __repr__(self):
        return f"BOOKING_DETAILS('{self.booking_id}')"


class BillingDetails(db.Model):
    __tablename__ = "billing_details"
    bill_id = db.Column(db.Integer, primary_key = True, nullable=False)
    bill_date = db.Column(db.DateTime, nullable=False)
    bill_status = db.Column(db.Boolean, nullable=False)
    total_late_fee = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    book_id = db.Column(db.ForeignKey("booking_details.booking_id"), nullable=False)

    def __repr__(self):
        return f"BillingDetails('{self.bill_id}')"



@app.route('/customer/add', methods =["POST"])
def add_customer():
    data = request.get_json()

    dl_number = data.get("dl_number")
    if  dl_number is None or type(dl_number) != str:
        raise BadRequest("Invalid License number")
    dl_number_exist = Customer.query.filter_by(dl_number=dl_number).first()
    if dl_number_exist != None:
        raise BadRequest("This License number already used")

    name = data.get("name")
    if name == None:
        raise BadRequest("Empty name")
    
    email_id = data.get("email_id")
    if check_email(email_id) == False:
        raise BadRequest("Invalid Email")
    
    phone_number = data.get("phone_number")
    
    if phone_number is None or len(phone_number) != 11 or not phone_number.startswith("09"):
        raise BadRequest("Invalid phone number") 
    phone_number_exist = Customer.query.filter_by(phone_number=phone_number).first()
    if phone_number_exist != None:
        raise BadRequest("this phone number already used") 
    
    customer = Customer(dl_number=dl_number, name=name, email_id=email_id, phone_number=phone_number)
    db.session.add(customer)
    db.session.commit()

    return 'Customer added'

@app.route('/car/category/add', methods =["POST"])
def add_machine_type():
    data = request.get_json()

    no_of_person = data.get("no_of_person")
    if no_of_person == None or type(no_of_person) != int:
        raise BadRequest("Invalid number of passengers")
    
    category_name = data.get("category_name")
    if category_name == None:
        raise BadRequest("Empty category name")
    

    cost_per_day = data.get("cost_per_day")
    if cost_per_day == None :
        raise BadRequest("Empty daily cost")
    
    late_fee_per_hour = data.get("late_fee_per_hour")
    if late_fee_per_hour == None:
        raise BadRequest("Empty delay cost")
    
    car = Car_Category(category_name=category_name,no_of_person=no_of_person, cost_per_day=cost_per_day, late_fee_per_hour=late_fee_per_hour)
    db.session.add(car)
    db.session.commit()

    return "car category added"

@app.route('/location/add', methods =["POST"])
def add_place():
    data = request.get_json()

    location_id = data.get("location_id")
    if location_id == None or type(location_id) != int:
        raise BadRequest("Invalid location id")

    location_name = data.get("location_name")
    if location_name == None or type(location_name) != str:
        raise BadRequest("Invalid location name")
    
    street = data.get("street")
    if street == None or type(street) != str:
        raise BadRequest("Empty street")
    
    city = data.get("city")
    if city == None or type(city) != str:
        raise BadRequest("Empty city")
    
    state_name = data.get("state_name")
    if state_name == None or type(state_name) != str:
        raise BadRequest("Empty state name")
    
    post_code = data.get("post_code")
    if post_code == None or type(post_code) != str:
        raise BadRequest("Empty post code")


    location_details = LocationDetails(location_id=location_id, location_name=location_name, street=street,
                                city=city, state_name=state_name, post_code=post_code)
    db.session.add(location_details)
    db.session.commit()
    return "A new location added"


@app.route('/car/add', methods =["POST"])
def add_car():
    data = request.get_json()

    registration_number = data.get("registration_number")
    if registration_number == None:
        raise BadRequest("Empty registration number")

    availability_flag = data.get("availability_flag")
    if type(availability_flag) != bool or availability_flag == None:
        raise BadRequest("Invalid reserved type")
    
    model_name = data.get("model_name")
    if model_name == None or type(model_name) != str:
        raise BadRequest("Invalid model name")
    
    loc_id = data.get("loc_id")
    if loc_id == None:
        raise BadRequest("Invalid loc id")
       
    car_categories = data.get("car_categories")
    if car_categories == None:
        raise BadRequest("Invalid car categories")

    maker = data.get("maker")
    if maker == None:
        raise BadRequest("Empty maker")
    
    kilometers = data.get("kilometers")
    if type(kilometers) != int or kilometers == None:
        raise BadRequest("Invalid odometer type")
    
    car = Car(registration_number=registration_number, availability_flag=availability_flag, model_name=model_name,
                loc_id=loc_id,car_categories=car_categories , maker=maker, kilometers=kilometers)
    db.session.add(car)
    db.session.commit()

    return "Car added"


@app.route('/car/rental/insurance', methods =["POST"])
def machine_rental_Insurance():
    data = request.get_json()

    insurance_code = data.get("insurance_code")
    if insurance_code is None or type(insurance_code) != int:
            raise BadRequest("Invalid insurance code ")

    insurance_name = data.get("insurance_name")
    if insurance_name == None:
        raise BadRequest("Empty insurance name")
    
    coverage_type = data.get("coverage_type")
    if coverage_type == None:
        raise BadRequest("Empty coverage type")

    cost_per_day = data.get("cost_per_day")
    if cost_per_day == None:
        raise BadRequest("Empty cost per day")


    new_machine_rental_Insurance = RentalCarInsurance(insurance_code=insurance_code, insurance_name=insurance_name,
                                                        coverage_type=coverage_type, cost_per_day=cost_per_day)
    db.session.add(new_machine_rental_Insurance)
    db.session.commit()

    return "A new car rental Insurance added"



@app.route('/booking', methods =["POST"])
def reservation():
    data = request.get_json()

    booking_id = data.get("booking_id")
    if booking_id == None :
        raise BadRequest("Empty book id")

    from_dt_time = data.get("from_dt_time")
    if from_dt_time == None :
        raise BadRequest("Empty from_dt_time")
    
    ret_dt_time = data.get("ret_dt_time")
    if ret_dt_time == None :
        raise BadRequest("Empty ret_dt_time")
    
    reservation_status = data.get("reservation_status")
    if type(reservation_status) != bool or reservation_status == None:
        raise BadRequest("Invalid reservation status")
    
    pickup_loc = data.get("pickup_loc")
    if pickup_loc == None :
        raise BadRequest("Empty pickup loc")
    
    reg_num = data.get("reg_num")
    if reg_num == None :
        raise BadRequest("Empty reg_num")
    
    dl_num = data.get("dl_num")
    if pickup_loc == None :
        raise BadRequest("Empty dl_num")
    
    ins_code = data.get("ins_code")
    if ins_code == None :
        raise BadRequest("Empty ins_code")

    booking_details = BookingDetails(booking_id=booking_id,from_dt_time=datetime.strptime(from_dt_time,'%Y-%m-%d'),
                                    ret_dt_time=datetime.strptime(ret_dt_time,'%Y-%m-%d'), reservation_status=reservation_status,
                                    pickup_loc=pickup_loc,reg_num=reg_num, dl_num=dl_num, ins_code=ins_code)
    db.session.add(booking_details)
    db.session.commit()

    return "A new booking details added."


@app.route('/bill/add', methods =["POST"])
def add_invoice():
    data = request.get_json()

    bill_id = data.get("bill_id")
    if bill_id == None:
        raise BadRequest("Empty bill_id")

    bill_date = data.get("bill_date")
    if bill_date == None:
        raise BadRequest("Empty bill date ")
    
    bill_status = data.get("bill_status")
    if type(bill_status) != bool or bill_status == None:
        raise BadRequest("Invalid bill_status")
    
    total_late_fee = data.get("total_late_fee")
    if total_late_fee == None:
        raise BadRequest("Empty total_late_fee")
    
    total_amount = data.get("total_amount")
    if total_amount == None:
        raise BadRequest("Empty total amount")
    
    book_id = data.get("book_id")
    if book_id == None:
        raise BadRequest("Empty book id")
    
     
    new_bill = BillingDetails(bill_id=bill_id, bill_date=datetime.strptime(bill_date,'%Y-%m-%d'), bill_status=bill_status,
                                   total_late_fee=total_late_fee, total_amount=total_amount, book_id=book_id)
    db.session.add(new_bill)
    db.session.commit()

    return "A new bill added"


@app.route('/car/<registration_number>/show', methods =["GET"])
def show_car(registration_number):

    car = Car.query.filter_by(registration_number=registration_number).first()
    if car == None :
        raise BadRequest("Nothing found")

    car_details = {"availability_flag": car.availability_flag,
                   "model_name": car.model_name,
                   "maker": car.maker,
                   "kilometers":car.kilometers}

    return jsonify(car_details)

@app.route('/customer/<dl_number>/show', methods =["GET"])
def show_customer(dl_number):

    customer = Customer.query.filter_by(dl_number=dl_number).first()
    if dl_number == None :
        raise BadRequest("Nothing found")

    customer_details = {"name": customer.name,
                   "email_id": customer.email_id,
                   "phone_number": customer.phone_number}

    return jsonify(customer_details)


@app.route('/location/<loc_id>/show', methods =["GET"])
def show_location(loc_id):

    location = LocationDetails.query.filter_by(location_id=loc_id).first()
    if location == None :
        raise BadRequest("Nothing found")

    location_details = {"street": location.street,
                   "city": location.city,
                   "state_name": location.state_name}

    return jsonify(location_details)


@app.route('/car/category/<category_name>/show', methods =["GET"])
def show_car_category(category_name):

    car_category = Car_Category.query.filter_by(category_name=category_name).first()
    if car_category == None :
        raise BadRequest("Nothing found")

    car_category_details = {"no_of_person": car_category.no_of_person,
                   "cost_per_day": car_category.no_of_person}

    return jsonify(car_category_details)


@app.route('/book/<book_id>/show', methods =["GET"])
def show_booking_details(book_id):

    booking = BookingDetails.query.filter_by(booking_id=book_id).first()
    if booking == None :
        raise BadRequest("Nothing found")

    booking_details = {"from_dt_time": booking.from_dt_time,
                   "ins_code": booking.ins_code,
                   "dl_num": booking.dl_num ,
                   "reg_num": booking.reg_num,
                   "pickup_loc": booking.pickup_loc}

    return jsonify(booking_details)





@app.route('/car/rental/<insurance_code>/show', methods =["GET"])
def show_rental_car_insurance_details(insurance_code):

    rental_car_insurance = RentalCarInsurance.query.filter_by(insurance_code=insurance_code).first()
    if rental_car_insurance == None :
        raise BadRequest("Nothing found")

    rental_car_insurance_details = {"coverage_type": rental_car_insurance.coverage_type,
                   "insurance_name": rental_car_insurance.insurance_name,
                   "cost_per_day": rental_car_insurance.cost_per_day}

    return jsonify(rental_car_insurance_details)


@app.route('/bill/<bill_id>/show', methods =["GET"])
def show_bill(bill_id):

    bill = BillingDetails.query.filter_by(bill_id=bill_id).first()
    if bill == None :
        raise BadRequest("Nothing found")

    bill_details = {"bill_status": bill.bill_status,
                   "bill_date": bill.bill_date,
                   "total_amount": bill.total_amount,
                   "book_id": bill.book_id}

    return jsonify(bill_details)
