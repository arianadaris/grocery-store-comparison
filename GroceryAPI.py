from flask import Blueprint, jsonify
import requests


import os
from dotenv import load_dotenv

api_bp = Blueprint('api', __name__)

load_dotenv()
API_KEY = os.getenv('GEOCODE_API_KEY')
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/zip?zip="

@api_bp.route('/')
def api():
    return jsonify(list(range(5)))


# Helper function
# Get coordinates from zipcode input
def getCoords(zipCode):
    request_url = f'{GEOCODE_URL}{zipCode}&limit=1&appid={API_KEY}'
    r = requests.request("GET", request_url, headers={}, data={})
    zip_data = r.json()

    coords = {
        'name': zip_data['name'],
        'longitude': zip_data['lon'],
        'latitude': zip_data['lat'],
    }

    return coords
    