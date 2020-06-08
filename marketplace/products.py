from flask import Blueprint, render_template
from .models import Product, Comment

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/<id>')
def item_details(id):
    product = get_product()
    return render_template('item_details.html', product=product)

def get_product():
    return product