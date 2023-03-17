from flask import Flask, render_template, request, flash, redirect, url_for, session
# flash() function - stores flashed messages in client's browser session, requires secret key
# secret key used to secure sessions
# user can access info stored in session, cannot modify it

import os
from datetime import timedelta

from extensions import db
from GroceryAPI import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "35238e7d4ac5422360b107255fbd18a9eab2d5aa0ae68c20"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///products.sqlite3"
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# Register API
app.register_blueprint(api_bp, url_prefix='/api')

# Connect to db
db.init_app(app)

from Models import *

@app.route('/', methods=['GET', 'POST'])
def get_home():
    if request.method == 'POST':
        
        zipCode = request.form['zipCode']
        if(len(zipCode) >= 5 and zipCode.isdigit()):
            coords = getCoords(zipCode)
            session.permanent = True
            session["longitude"] = coords['longitude']
            session["latitude"] = coords['latitude']
            session["name"] = coords['name']
        else:
            flash('Please input a valid zip code.')
    name = ""
    if 'name' in session:
        name = session['name']
    return render_template("home.html", name=name)

@app.route('/products', methods=['GET', 'POST'])
def get_view():
    # name = ""
    # if request.method == 'POST':
    #     name = request.form['name']
    #     product = products(name)
    #     db.session.add(product)
    #     db.session.commit()
    #     redirect(url_for('get_view'))

    query = ""

    if request.method == "POST":
        query = request.form['name'].replace(" ", "+")
        result = get_target_tcin(query)
        print('Success' if result else 'Failure')
    
    return render_template('products.html', products=products.query.all())

@app.route('/products/delete/<int:id>')
def get_delete_product(id):
    product_to_delete = products.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
    except Exception as e:
        print(e)

    return redirect(url_for('get_view'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True, port=5001)