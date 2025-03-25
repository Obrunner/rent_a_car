from app import db

class Customer():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class CustomersModel():

    def getAllCustomers(self):
        customers = []
        
        rows = db.executeSELECT('SELECT * FROM customers')
        for row in rows:
            customers.append(Customer(row[0], row[1]))

        return customers

    def createCustomer(self, name):
        db.executeChanges(f'''
            INSERT INTO customers (name)
            VALUES ('{name}')
        ''')

    def updateCustomer(self):
        pass

    def deleteCustomer(self, id):
        db.executeChanges(f'''
           DELETE FROM customers WHERE id={id}
        ''')

class Car():
    def __init__(self, id, model, totalKilometers):
        self.id = id
        self.model = model
        self.totalKilometers = totalKilometers

class CarsModel():

    def getAllCars(self):
        cars = []
        
        rows = db.executeSELECT('SELECT * FROM cars')
        for row in rows:
            cars.append(Car(row[0], row[1], row[2]))

        return cars

    def getAvailableCars(self):
        cars = []
        
        rows = db.executeSELECT('''
           SELECT * FROM cars 
            WHERE id NOT IN (
                SELECT car_id 
                FROM rental_agreements 
                WHERE is_open = 1
            );
        ''')

        for row in rows:
            cars.append(Car(row[0], row[1], row[2]))

        return cars

    def createCar(self, model, totalKilometers):
        db.executeChanges(f'''
            INSERT INTO cars (model, km)
            VALUES ('{model}', {totalKilometers})
        ''')

    def updateCar(self):
        pass

    def deleteCar(self, id):
        db.executeChanges(f'''
           DELETE FROM cars WHERE id={id}
        ''')

class RentalAgreement():
    def __init__(self, id, km_allowance, car, customer, is_open):
        self.id = id
        self.kmAllowance = km_allowance
        self.car = car
        self.customer = customer
        self.isOpen = is_open

class RentalAgreementModel():

    def getAllRentalAgreements(self):
        agreements = []
        
        rows = db.executeSELECT('SELECT * FROM rental_agreements')
        for row in rows:
            agreements.append(RentalAgreement(row[0], row[1], row[2], row[3] == 1))

        return agreements

    def getAllOpenAgreements(self):
        agreements = []
        
        rows = db.executeSELECT(
            '''SELECT * FROM rental_agreements
                INNER JOIN cars ON rental_agreements.car_id = cars.id
                INNER JOIN customers ON rental_agreements.customer_id = customers.id
                WHERE is_open = 1
            ''')

        for row in rows:
            car = Car(row[5], row[6], row[7])
            customer = Customer(row[8], row[9])
            agreements.append(RentalAgreement(row[0], row[1], car, customer, row[4] == 1))

        return agreements

    def createRentalAgreement(self, km_allowance, car_id, customer_id):
        db.executeChanges(f'''
            INSERT INTO rental_agreements (km_allowance, car_id, customer_id, is_open)
            VALUES ({km_allowance}, {car_id}, {customer_id}, 1)
        ''')