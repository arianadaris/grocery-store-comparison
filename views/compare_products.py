from flask import Blueprint, render_template
import requests

compare_bp = Blueprint('compare', __name__)

port = 5002
api_url = f'http://127.0.0.1:{port}/api/'

@compare_bp.route('/')
def get_compare_view():
    return render_template('compare.html', keywords=get_keywords())

@compare_bp.route('/<keyword>')
def compare_keyword(keyword):
    # Get Target products that match the given keyword
    r = requests.request("GET", f'{api_url}target/{keyword}')
    target_products = r.json()

    return render_template('compare.html', keywords=get_keywords(), filter=[keyword])

# Helper function
def get_keywords():
    r = requests.request('GET', api_url+'products/keywords', headers={}, data={})
    return r.json()