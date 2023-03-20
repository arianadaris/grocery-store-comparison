from flask import Blueprint, render_template
import requests

compare_bp = Blueprint('compare', __name__)

port = 5002
api_url = f'http://127.0.0.1:{port}/api/'

@compare_bp.route('/')
def get_compare_view():
    return render_template('compare.html', keywords=get_keywords(), products=[])

@compare_bp.route('/<keyword>')
def compare_keyword(keyword):
    # Get all products that match the given word
    r = requests.request("GET", f'{api_url}filter/{keyword}')
    all_products = r.json()

    storeKeys = get_stores(all_products)

    zipcode = '85201'

    # For each store in all products
    for index, store in enumerate(all_products):
        products_list = store[storeKeys[index]]
        products_with_prices = []

        for product in products_list:
            r = requests.request("GET", f'{api_url}prices/id={product["id"]}&zip={zipcode}')
            products_with_prices.append(r.json())
            
        all_products[storeKeys[index]] = products_with_prices

    return render_template('compare.html', keywords=get_keywords(), filter=[keyword], products=all_products)

# Helper function
def get_keywords():
    r = requests.request('GET', api_url+'products/keywords', headers={}, data={})
    return r.json()

def get_stores(products):
    def get_keys(store):
        return list(store.keys())[0]
    
    return list(map(get_keys, products))
