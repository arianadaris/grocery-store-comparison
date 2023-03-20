from flask import Blueprint
import requests
from dotenv import load_dotenv
import os

load_dotenv()
GEOCODE_API_KEY = os.getenv('GEOCODE_API_KEY')
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/zip?zip="

geocode_api_bp = Blueprint('api/geocode', __name__)

"""
URL - /api/coords/12345
    Parameters - zipcode: int - 5 digit zipcode
    Returns - dictionary containing the location, latitude, longitude near that zipcode
"""
@geocode_api_bp.route('/<int:zipcode>')
def get_coords(zipcode):
    request_url = f'{GEOCODE_URL}{zipcode}&limit=1&appid={GEOCODE_API_KEY}'
    r = requests.request("GET", request_url, headers={}, data={})
    zip_data = r.json()

    coords = {
        'name': zip_data['name'],
        'longitude': zip_data['lon'],
        'latitude': zip_data['lat'],
        'zipcode': zipcode
    } 

    return coords  