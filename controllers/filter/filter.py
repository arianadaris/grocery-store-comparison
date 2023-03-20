from flask import Blueprint

from __main__ import db
from models.db_manager import *

filter_bp = Blueprint('filter', __name__)

@filter_bp.route('/<keyword>')
def get_products_by_keyword(keyword):
    # Goal is to return a list of containing a dictionary for each store, which contains a dictionary of all products

    all_products = []

    stores = [
        'Target',
        'Trader Joes'
    ]

    # For each store in the list, create a dictionary for that store 
    keyword = keyword.title().replace('+', ' ')
    for store in stores:
        store_dict = {}

        if store == 'Target':
            products_list = products.query.filter(products.target_tcin != 0, products.keyword == keyword)
        elif store == 'Trader Joes':
            products_list = products.query.filter(products.traderjoes_sku != 0, products.keyword == keyword)

        store_dict[store] = [product.as_dict() for product in products_list]
        all_products.append(store_dict)
        
    return all_products

@filter_bp.route('/target/')
@filter_bp.route('/target/<keyword>')
def get_target_products(keyword=None):
    if keyword:
        print('Filtering by specific products')
        target_products = products.query.filter(products.target_tcin != 0, products.keyword == keyword).all()
    else:
        print('Filtering by store')
        target_products = products.query.filter(products.target_tcin != 0).all()

    return [product.as_dict() for product in target_products]

@filter_bp.route('/trader_joes')
@filter_bp.route('/trader_joes/<keyword>')
def get_trader_joes_products(keyword=None):
    if keyword:
        print('Filtering by specific products')
        trader_joes_products = products.query.filter(products.traderjoes_sku != 0, products.keyword == keyword).all()
    else:
        trader_joes_products = products.query.filter(products.traderjoes_sku != 0).all()
        print('Filtering by store')

    return [product.as_dict() for product in trader_joes_products]