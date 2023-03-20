from flask import Flask
from datetime import timedelta
from controllers.database import db

# Import Views
from views.home import *
from views.products import *
from views.compare_products import *

# Import APIs and Controllers
from controllers.products_api import *
from controllers.prices_api import *
from controllers.geocode_api import *
from controllers.filter.autocomplete import *
from controllers.filter.filter import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "35238e7d4ac5422360b107255fbd18a9eab2d5aa0ae68c20"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///products.sqlite3"
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# Register URL blueprints
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(compare_bp, url_prefix='/compare')

# Register API
app.register_blueprint(geocode_api_bp, url_prefix='/api/geocode')
app.register_blueprint(products_api_bp, url_prefix='/api/products')
app.register_blueprint(prices_api_bp, url_prefix='/api/prices')
app.register_blueprint(autocomplete_bp, url_prefix='/api/autocomplete')
app.register_blueprint(filter_bp, url_prefix='/api/filter')

port = 5002

# Connect to db
db.init_app(app)

from models.db_manager import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=port)