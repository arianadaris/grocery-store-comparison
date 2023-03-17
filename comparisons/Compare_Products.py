from flask import Blueprint, render_template

compare_bp = Blueprint('compare', __name__)

@compare_bp.route('/')
def get_compare_view():
    return render_template('compare_products.html')