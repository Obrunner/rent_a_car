from flask import request, jsonify
from app import app
from app.model import CustomersModel

customers_model = CustomersModel()

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data['name']

    customers_model.createCustomer(name)

    return jsonify({'message': 'Car created successfully'}), 200

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = customers_model.getAllCustomers()
    return jsonify([{'id': customer.id, 'name': customer.name} for customer in customers])


@app.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customers(customer_id):
    customers_model.deleteCustomer(customer_id)

    return jsonify({'message': 'Customer deleted successfully'}), 200