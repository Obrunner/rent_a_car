from flask import Flask

from app.database_connector import DatabaseConnector

app = Flask(__name__)
db = DatabaseConnector()

from app import car_routes
from app import customer_routes
from app import rental_routes