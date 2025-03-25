from flask import request, jsonify
from app import app
from app.model import RentalAgreementModel

rental_agreement_model = RentalAgreementModel()

@app.route('/rentals', methods=['POST'])
def create_rental_agreement():
    data = request.get_json()
    km_allowance = data['kmAllowance']
    car_id = data['carId']
    customer_id = data['customerId']

    rental_agreement_model.createRentalAgreement(km_allowance, car_id, customer_id)

    return jsonify({'message': 'Rental agreement created successfully'}), 200

@app.route('/rentals/open', methods=['GET'])
def get_open_rental_agreements():
    agreements = rental_agreement_model.getAllOpenAgreements()
    return jsonify([{'renter': 
                     {'id': agreement.customer.id, 'name': agreement.customer.name}, 
                     'car': 
                     {'id': agreement.car.id, 'model': agreement.car.model, 'totalKilometers': agreement.car.totalKilometers},
                     'kmAllowance': agreement.kmAllowance, 
                     'isOpen': agreement.isOpen} for agreement in agreements])