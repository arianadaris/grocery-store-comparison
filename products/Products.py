from flask import Blueprint, request, render_template, flash, redirect, url_for
import requests

products_bp = Blueprint('products', __name__)

port = 5002
api_url = f'http://127.0.0.1:{port}/api/'

@products_bp.route('')
def get_products():
    products = []

    # Call API to retrieve data from database
    if request.method == "GET":
        r = requests.request('GET', api_url+'products', headers={}, data={})
        products = r.json()

    return render_template('products.html', products=products)

@products_bp.route('/add-by-query', methods=['POST'])
def get_add_by_query():
    if(request.form['name'] != ''):
        query = request.form['name'].replace(" ", "+")

        r = requests.request('GET', f'{api_url}products/search/q={query}')
        result = r.json()
        
        r = requests.request('GET', api_url+'products', headers={}, data={})
        products = r.json()

        if result['success'] == "True":
            flash(f'Products successfully added by query!', 'text-success')
        else:
            flash(f'Add By Query Failed: {result}', 'text-danger')
        
        return render_template('products.html', products=products)
        
    return redirect(url_for('get_products'))

@products_bp.route('/delete/<int:id>')
def get_delete_product(id):
    # Call API to retrieve product from database
    r = requests.request('GET', f'{api_url}products/delete/{id}')
    result = r.json()

    r = requests.request('GET', api_url+'products', headers={}, data={})
    products = r.json()

    if result['success'] == "True":
        flash(f'Product {id} successfully deleted!', 'text-success')
    else:
        flash(f'Delete {id} Failed: {result}', 'text-danger')
    
    return render_template('products.html', products=products)

@products_bp.route('/delete')
def get_delete_all():
    # Call API to delete all products from the database
    r = requests.request('GET', f'{api_url}products/delete')
    result = r.json()

    r = requests.request('GET', api_url+'products', headers={}, data={})
    products = r.json()

    if result['success'] == "True":
        flash(f'All products successfully deleted!', 'text-success')
    else:
        flash(f'Delete All Failed: {result}', 'text-danger')

    return render_template('products.html', products=products)