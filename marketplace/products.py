from flask import Blueprint, render_template

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/<id>')
def item_details(id):
    return render_template('products/item_details.html')