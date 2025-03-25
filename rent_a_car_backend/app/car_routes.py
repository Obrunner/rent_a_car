from flask import request, jsonify
from app import app
from app.model import CarsModel

cars_model = CarsModel()

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    model = data['model']
    totalKilometers = data['totalKilometers']

    cars_model.createCar(model, totalKilometers)

    return jsonify({'message': 'Car created successfully'}), 200

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = cars_model.getAllCars()
    return jsonify([{'id': car.id, 'model': car.model, 'totalKilometers': car.totalKilometers} for car in cars])

@app.route('/cars/available', methods=['GET'])
def get_available_cars():
    cars = cars_model.getAvailableCars()
    return jsonify([{'id': car.id, 'model': car.model, 'totalKilometers': car.totalKilometers} for car in cars])

@app.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    cars_model.deleteCar(car_id)

    return jsonify({'message': 'Car deleted successfully'}), 200