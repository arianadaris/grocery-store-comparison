from flask import Blueprint

from __main__ import db
from models.db_manager import *

from models.target import Target
from models.trader_joes import Trader_Joes

prices_api_bp = Blueprint('api/prices', __name__)

"""
URL - /api/prices/id=1&lat=12.34&lon=12.45&zip=85201
    Given a product id, it retrieves the product's price from all appropriate stores
    Parameters -
        product_id: int - product identification number
        lat: string - latitude
        lon: string - longitude
        zipcode: string - 5 digit zipcode number
    Returns - dictionary containing product information and prices for various stores
"""
@prices_api_bp.route('/id=<int:product_id>&lat=<lat>&lon=<lon>&zip=<zipcode>')
def get_price(product_id, lat, lon, zipcode):
    product = products.query.get_or_404(product_id)

    if product.target_tcin != '0':
        target_price = Target().get_price(product.target_tcin, zipcode)
    if product.traderjoes_sku != '0':
        traderjoes_price = Trader_Joes().get_price(product.traderjoes_sku)

    prices = {
        'name': product.name,
        'image': product.image,
        'id': product_id,
        'target_price': target_price if 'target_price' in locals() else 'N/A',
        'traderjoes_price': traderjoes_price if 'traderjoes_price' in locals() else 'N/A'
    }

    return prices