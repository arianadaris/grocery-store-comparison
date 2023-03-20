from flask import Blueprint, request, render_template, flash, redirect, url_for
import requests

products_bp = Blueprint('products', __name__)

port = 5002
api_url = f'http://127.0.0.1:{port}/api/'

@products_bp.route('')
def get_products():
    products = []

    # Call API to retrieve data from database
    r = requests.request('GET', api_url+'products', headers={}, data={})
    products = r.json()

    return render_template('products.html', products=products, keywords=get_keywords(), stores=get_stores())

@products_bp.route('/add-by-query', methods=['POST'])
def get_add_by_query():
    if(request.form['name'] != ''):
        query = request.form['name'].title().replace(" ", "+")

        r = requests.request('GET', f'{api_url}products/add/q={query}')
        result = r.json()
        
        r = requests.request('GET', api_url+'products', headers={}, data={})
        products = r.json()

        if result['success'] == "True":
            flash(f'Products successfully added by query!', 'text-success')
        else:
            flash(f'Add By Query Failed: {result}', 'text-danger')
        
        return render_template('products.html', products=products, keywords=get_keywords(), stores=get_stores())
        
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
    
    return render_template('products.html', products=products, keywords=get_keywords(), stores=get_stores())

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

    return render_template('products.html', products=products, keywords=get_keywords(), stores=get_stores())

@products_bp.route('/filter', methods=["GET", "POST"])
def filter_by_keyword():
    word = store = ""
    if request.method == "POST":
        if not 'keyword-dropdown' in request.form:
            word = list(request.form.keys())[0]
        if not 'store-dropdown' in request.form:
            store = list(request.form.keys())[1]

        if word == "" and store == "":
            return redirect(url_for('products.get_products'))

        filtered_products = []

        if word in get_stores() or store in get_stores():
            print(f'Getting {word} products from {store}')
            if word == 'Target' or store == 'Target':
                r = requests.request('GET', f'{api_url}filter/target/{word}')
            elif word == 'Trader Joes' or store == 'Trader Joes':
                r = requests.request('GET', f'{api_url}filter/trader_joes/{word}')
        else:
            print(f'Getting {word} products')
            query = word.replace(' ', '+')
            r = requests.request('GET', f'{api_url}filter/{query}')

        filtered_products = r.json()

    return render_template('products.html', products=[filtered_products], filter=[word, store], keywords=get_keywords(), stores=get_stores())


## Helper function
def get_keywords():
    r = requests.request('GET', api_url+'products/keywords', headers={}, data={})
    return r.json()

def get_stores():
    return [
        'Target',
        'Trader Joes'
    ]