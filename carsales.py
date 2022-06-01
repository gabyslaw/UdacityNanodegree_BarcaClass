from flask import Flask, redirect, render_template, request
import psycopg2

carsales = Flask(__name__)


def connection():
    s = 'localhost' #server name
    d = 'vehicles' #database name
    u = 'postgres' # username
    p = 'password' #password
    conn = psycopg2.connect(host=s, database=d, user=u, password=p)
    return conn

@carsales.route('/')
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Barcars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render_template("carlist.html", cars = cars)

@carsales.route('/addcar', methods=['GET', 'POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Barcars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
        conn.commit()
        conn.close()
        return redirect('/')

@carsales.route('/updatecar/<int:id>', methods=['GET', 'POST'])
def updatecar(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Barcars WHERE id = %s", (str(id)))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render_template("addcar.html", car = cr[0])
    if request.method == 'POST':
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute("UPDATE Barcars SET name = %s, year = %s, price = %s where id = %s", (name, year, price, id))
        conn.commit()
        conn.close()
        return redirect('/')
    pass
    

if __name__ == '__main__':
    carsales.run(debug=True)