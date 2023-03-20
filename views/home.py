from flask import Blueprint, render_template, request, session, flash
import requests
import json

port = 5002

api_url = f'http://127.0.0.1:{port}/api/'

home_bp = Blueprint('', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def get_home():
    product_ids = [26, 27, 28]
    products = []

    if request.method == 'POST':
        zipcode = request.form['zipcode']

        # Form validation
        if(len(zipcode) >= 5 and zipcode.isdigit()):
            # Call API to retrieve keyword
            r = requests.request("GET", f'{api_url}geocode/{zipcode}')
            coords = r.json()

            session.permanent = True
            session["longitude"] = coords['longitude']
            session["latitude"] = coords['latitude']
            session["location"] = coords['name']
            session["zipcode"] = coords['zipcode']

            # If zipcode not in json file, add zipcode to json file
            zipcodes = json.load(open('./controllers/filter/zipcodes.json'))
            if not zipcode in zipcodes:
                zipcodes.append(zipcode)
                with open('./autocomplete/zipcodes.json', 'w') as f:
                    f.write(json.dumps(zipcodes))
                
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