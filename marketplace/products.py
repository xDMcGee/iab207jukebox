from flask import Blueprint, render_template, request
from .models import Product, Comment
from .forms  import ProductForm

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/<id>')
def item_details(id):
    # product = get_product()
    return render_template('item_details.html')

@bp.route('/create', methods=['GET','POST'])
def create():
    print('Method type', request.method)
    form = ProductForm()
    if form.validate_on_submit():
        print('Succesfully create new product', 'success')

    return render_template('components/create_product.html', form=form)

# def get_product():
#     return product