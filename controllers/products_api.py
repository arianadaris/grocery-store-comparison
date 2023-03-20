from flask import Blueprint
from operator import itemgetter

from __main__ import db
from models.db_manager import *

from models.target import Target
from models.trader_joes import Trader_Joes

products_api_bp = Blueprint('api/products', __name__)

"""
URL - /api/products
    Returns - dictionary containing all of the products in the products table
"""
@products_api_bp.route('/', methods=['GET'])
def get_products():
    all_products = []

    stores = [
        'Target',
        'Trader Joes'
    ]

    for store in stores:
        store_dict = {}

        if store == 'Target':
            products_list = products.query.filter(products.target_tcin != '0').all()
        elif store == 'Trader Joes':
            products_list = products.query.filter(products.traderjoes_sku != '0').all()

        store_dict[store] = [product.as_dict() for product in products_list]
        all_products.append(store_dict)
        
    return all_products

"""
URL - /api/products/1
    Returns - dictionary containing the product with the inputted ID
"""
@products_api_bp.route('/<int:id>')
def get_product(id):
    product = products.query.get_or_404(id)
    return product.as_dict()

"""
URL - /api/products/delete
    Deletes all products in the products table
    Returns - dictionary containing a success value and optional error string
"""
@products_api_bp.route('/delete')
def delete_all():
    try:
        db.session.query(products).delete()
        db.session.commit()
        return {
            'success': 'True',
            'error': 'N/A'
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': 'False',
            'error': str(e)
        }

"""
URL - /api/products/delete/1
    Deletes the product with the inputted ID from the products table
    Returns - dictionary containing a success value and optional error string
"""
@products_api_bp.route('/delete/<int:id>')
def delete_product(id):
    product = products.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return {
            'success': 'True',
            'error': 'N/A'
        }
    except Exception as e:
        return {
            'success': 'False',
            'error': str(e)
        }

"""
URL - /api/products/search/orange+juice
    Given a query string, it searches the query through Target and retrieves all products related to that query string.
    For each product retrieved, it formats the product into the Product model and adds it to the products table.
    Parameters - query: string - used for specifying the product search
    Returns - dictionary containing a success value and optional error string
"""
# Defines a route add that allows the user to search and add Products to the database based on a general query
# EX. keyword = orange juice
@products_api_bp.route('/add/q=<query>')
def add_products(query):
    try:
        # Get products from Target
        target_products = Target().get_products(query)
        trader_joes_products = Trader_Joes().get_products(query)

        add_products_to_db(target_products, 'Target')
        add_products_to_db(trader_joes_products, 'Trader Joes')

        return {
            'success': 'True',
            'error': 'N/A'
        }
    except Exception as e:
        return {
            'success': 'False',
            'error': 'Adding By Query Failed: ' + str(e)
        }

@products_api_bp.route('/keywords')
def get_keywords():
    all_products = products.query.with_entities(products.keyword.distinct()).all()
    keywords = [product[0] for product in all_products]
    return keywords

## Helper function
def add_products_to_db(all_products, store):
    for product in all_products:
        name, image, keyword, weight = itemgetter('name', 'image', 'keyword', 'weight')(product)
        product_obj = products(name, image, keyword, weight)

        if store == 'Target':
            product_obj.set_target_tcin(product["tcin"])
        if store == 'Trader Joes':
            product_obj.set_traderjoes_sku(product['sku'])

        db.session.add(product_obj)
        db.session.commit()