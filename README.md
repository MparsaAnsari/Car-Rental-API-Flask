# Car-Rental-API-Flask
A  RESTful API for a car rental system built with Flask, SQLAlchemy, and PostgreSQL, featuring a normalized database schema and complete CRUD operations.
Car Rental System API (English)
This project is the backend RESTful API for a comprehensive car rental system, built with Python, Flask, and SQLAlchemy, and designed to work with a PostgreSQL database. The system manages customers, cars, locations, bookings, and billing through a set of well-defined API endpoints.

The database schema is designed based on a detailed ER diagram and is normalized to the Third Normal Form (3NF) to ensure data integrity and reduce redundancy.

✨ Features & Functionality
Complete CRUD Operations: The API provides endpoints to Create, Read, Update, and Delete records for all major entities.

Entity Management:

Customers: Manage customer information, including name, driver's license, and contact details.

Cars: Manage the fleet of cars, including model, maker, availability, and location.

Car Categories: Define different categories of cars (e.g., Economy, SUV, Luxury) with specific pricing and fees.

Locations: Manage pickup and drop-off locations.

Insurance: Manage optional rental insurance plans.

Core Business Logic:

Booking System: Create and manage reservations, linking customers, cars, and locations.

Billing System: Generate bills for bookings, calculating total costs and late fees.

Data Validation: Input data for all endpoints is validated to ensure correctness (e.g., valid email format, phone number).

🛠️ Technologies Used
Backend: Python, Flask

ORM: SQLAlchemy, Flask-Migrate

Database: PostgreSQL

API Testing: (e.g., Postman, Insomnia)

Database Schema
The database consists of 7 normalized tables:

Customer: Stores customer details.

Car_Category: Defines car types and their rates.

LocationDetails: Stores rental office locations.

Car: Contains details of each car in the fleet.

RentalCarInsurance: Stores available insurance plans.

BookingDetails: The central table for managing reservations.

BillingDetails: Stores billing information related to a booking.

(For the detailed schema and relationships, please refer to the schema.sql file.)

🚀 API Endpoints
The API provides various endpoints for interacting with the system. Here are some examples:

POST /customer/add: Add a new customer.

POST /car/add: Add a new car to the fleet.

POST /booking: Create a new booking.

POST /bill/add: Add a new bill.

GET /customer/<dl_number>/show: Get details of a specific customer.

GET /car/<registration_number>/show: Get details of a specific car.

... and many more for all other entities.

⚙️ How to Set Up and Run
Clone the repository:

git clone [Your GitHub Repository URL]

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:

pip install -r requirements.txt

Set up the PostgreSQL database:

Make sure you have PostgreSQL installed and running.

Create a new database (e.g., rentalcar).

Update the database connection string in app.py if needed:
'postgresql://username:password@localhost:5432/yourdbname'

Create the database tables:

flask db upgrade

(Alternatively, you can run the commands in the schema.sql file directly in your database.)

Run the Flask application:

flask run

The API will be running at http://127.0.0.1:5000.
