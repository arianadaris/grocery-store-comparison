from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import timedelta
import requests
from extensions import db

# Import blueprints
from api.GroceryAPI import *
from products.Products import *
from comparisons.Compare_Products import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "35238e7d4ac5422360b107255fbd18a9eab2d5aa0ae68c20"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///products.sqlite3"
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# Register URL blueprints
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(compare_bp, url_prefix='/compare')

# Register API
app.register_blueprint(api_bp, url_prefix='/api')
port = 5002
api_url = f'http://127.0.0.1:{port}/api/'

# Connect to db
db.init_app(app)

from Models import *

@app.route('/', methods=['GET', 'POST'])
def get_home():
    product_ids = [1,2,3]
    products = []

    if request.method == 'POST':
        zipcode = request.form['zipcode']

        # Form validation
        if(len(zipcode) >= 5 and zipcode.isdigit()):
            # Call API to retrieve keyword
            r = requests.request("GET", f'{api_url}coords/{zipcode}')
            coords = r.json()

            session.permanent = True
            session["longitude"] = coords['longitude']
            session["latitude"] = coords['latitude']
            session["location"] = coords['name']
            session["zipcode"] = coords['zipcode']
        else:
            flash('Please input a valid zip code.')

    location = ""
    if 'location' in session:
        location = session['location']
        latitude = session['latitude']
        longitude = session['longitude']
        zipcode = session['zipcode']

        for product_id in product_ids:
            r = requests.request('GET', f'{api_url}prices/id={product_id}&lat={latitude}&lon={longitude}&zip={zipcode}')

            products.append(r.json())

    return render_template("home.html", name=location, products=products)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True, port=port)