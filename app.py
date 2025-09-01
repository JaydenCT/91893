

from flask import Flask, g, render_template, request  # type: ignore
import sqlite3
from flask import g # type: ignore


app = Flask(__name__)

DATABASE = 'database_cars.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET"])
def index():
    cursor = get_db().cursor()
    sql = '''
    SELECT Manufacturer.name, model, year, kms, price, type FROM cars
    JOIN Transmission
    ON Cars.transmission = Transmission.id
    JOIN Manufacturer
    ON Cars.manufacturer_id = Manufacturer.id
    ORDER BY Manufacturer.name, model
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("home.html", cars=results)

@app.route("/home2", methods=["GET"])
def home():
    return render_template("home2.html")

@app.route("/cars")
def cars():
    cursor = get_db().cursor()
    sql = '''
    SELECT Manufacturer.name, model, year, kms, price, type FROM cars
    JOIN Transmission
    ON Cars.transmission = Transmission.id
    JOIN Manufacturer
    ON Cars.manufacturer_id = Manufacturer.id
    ORDER BY Manufacturer.name, model
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    models_sql = '''
   SELECT DISTINCT model FROM Cars ORDER BY model;
    '''
    cursor.execute(models_sql)
    models = cursor.fetchall()

    return render_template ("cars.html" , cars=results, models=models)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/favourites")
def favourites():
    return render_template("favourites.html")

@app.route("/search")
def search():
    from flask import request # type: ignore
    query = request.args.get('q', '').strip()
    cars = []
    if query:
        cursor = get_db().cursor()
        sql = '''
        SELECT Manufacturer.name, model, year, kms, price, type FROM cars
        JOIN Transmission ON Cars.transmission = Transmission.id
        JOIN Manufacturer ON Cars.manufacturer_id = Manufacturer.id
        WHERE LOWER(Manufacturer.name || ' ' || model) = ?
        ORDER BY Manufacturer.name, model
        '''
        q = query.lower()
        cursor.execute(sql, (q,))
        cars = cursor.fetchall()
    return render_template("home.html", cars=cars, search_query=query)

if __name__ == "__main__":
    app.run()


