from flask import Flask, redirect, render_template, request, jsonify, abort
from flask_cors import cross_origin, CORS
import psycopg2
from flask_sqlalchemy import SQLAlchemy

carsales = Flask(__name__)
carsales.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/vehicles'
carsales.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(carsales)
db = SQLAlchemy(carsales)
#Models
class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key = True)
    car_name = db.Column(db.String(100), nullable = False)
    car_type = db.Column(db.String(100), nullable = False)
    car_year = db.Column(db.Integer(), nullable = False)
    car_price = db.Column(db.Float(), nullable = False)
    car_description = db.Column(db.String(500), nullable = False)
    car_number_plate =  db.Column(db.String(500), nullable = False, unique=True)

    def __repr__(self):
        return "<Car %r>" % self.car_name

    def format(self):
        return {
            'car_name': self.car_name,
            'car_type': self.car_type,
            'car_year': self.car_year,
            'car_price': self.car_price,
            'car_description': self.car_description
        }

db.create_all()

@carsales.route('/')
def main():
    return jsonify({"message": "Welcome to my hooooood"})

#Create POST route

@cross_origin()
@carsales.route('/addcar', methods=['POST'])
def addcar():
    try:
        car_data = request.json

        car_name = car_data['car_name']
        car_type = car_data['car_type']
        car_year= car_data['car_year']
        car_price = car_data['car_price']
        car_description = car_data['car_description']
        car_number_plate = car_data['number_plate']

        car = Car(car_name=car_name, car_type=car_type, car_year=car_year, car_price=car_price, car_description=car_description, car_number_plate=car_number_plate)
        db.session.add(car)
        db.session.commit()

        #TODO: add a new column to the table (number_plate) and ensure the car data doesn't 
        # get saved if a number plate exists in the database
        return jsonify({
            "success": True,
            "response": "Car successfully added"
        })
    except:
        db.session.rollback()
        abort(401)
    finally:
        db.session.close

@cross_origin()
@carsales.route('/getcar', methods=['GET'])
def getcar():
    all_cars = []
    cars = Car.query.all() 
    
    for car in cars:
        result = {
            "car_id": car.id,
            "car_name": car.car_name,
            "car_type": car.car_type,
            "car_year": car.car_year,
            "car_price": car.car_price,
            "car_description": car.car_description,
        }
        all_cars.append(result)

    
    return jsonify({
        "success": True,
        "cars": all_cars,
        "total_cars": len(cars)
    })
    
#TODO: Add a getcarbyid route
@carsales.route('/cars/<int:car_id>', methods=['DELETE'])
def getCar(car_id):
    try:
        car = Car.query.get(car_id).format()

        return jsonify({
            'success': True,
            'car': car
            })
    except:
        abort(404)


@carsales.route('/updatecar/<int:car_id>', methods=['PATCH'])
def updatecar(car_id):
    car = Car.query.get(car_id)

    car_name = request.json['car_name']
    car_type = request.json['car_type']
    car_price = request.json['car_price']

    if car is None:
        abort(404)
    else:
        car.car_name = car_name
        car.car_type = car_type
        car.car_price = car_price
        db.session.add(car)
        db.session.commit()

        return jsonify({
        "success": True,
        "response": "Car successfully updated"
    })

#TODO: implement the delete route
@carsales.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        car = Car.query.get(car_id)

        db.session.delete(car)
        db.session.commit()

        return jsonify({
            'success': True,
            'car': car.id
            })
    except:
        db.session.rollback()
    finally:
        db.session.close()


# def connection():
#     s = 'localhost' #server name
#     d = 'vehicles' #database name
#     u = 'postgres' # username
#     p = 'password' #password
#     conn = psycopg2.connect(host=s, database=d, user=u, password=p)
#     return conn

# @carsales.route('/')
# def main():
#     cars = []
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Barcars")
#     for row in cursor.fetchall():
#         cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
#     conn.close()
#     return render_template("carlist.html", cars = cars)

# @carsales.route('/addcar', methods=['GET', 'POST'])
# def addcar():
#     if request.method == 'GET':
#         return render_template("addcar.html", car = {})
#     if request.method == 'POST':
#         id = int(request.form["id"])
#         name = request.form["name"]
#         year = int(request.form["year"])
#         price = float(request.form["price"])
#         conn = connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO Barcars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
#         conn.commit()
#         conn.close()
#         return redirect('/')

# @carsales.route('/updatecar/<int:id>', methods=['GET', 'POST'])
# def updatecar(id):
#     cr = []
#     conn = connection()
#     cursor = conn.cursor()
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM Barcars WHERE id = %s", (str(id)))
#         for row in cursor.fetchall():
#             cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
#         conn.close()
#         return render_template("addcar.html", car = cr[0])
#     if request.method == 'POST':
#         name = request.form["name"]
#         year = int(request.form["year"])
#         price = float(request.form["price"])
#         cursor.execute("UPDATE Barcars SET name = %s, year = %s, price = %s where id = %s", (name, year, price, id))
#         conn.commit()
#         conn.close()
#         return redirect('/')
    
    
# @carsales.route('/deletecar/<int:id>')
# def deletecar(id):
#     conn = connection();
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Barcars WHERE id = %s", (str(id)))
#     conn.commit()
#     conn.close()
#     return redirect('/')

if __name__ == '__main__':
    carsales.run(debug=True)