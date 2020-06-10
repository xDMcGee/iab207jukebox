from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product, Comment
from .forms  import ProductForm
from . import db

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/<id>')
def show(id):
    product = Product.query.filter_by(id=id).first()
    return render_template('components/show.html', product = product)

@bp.route('/create', methods=['GET','POST'])
def create():
    print('Method type', request.method)
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(album_title = form.album_title.data,
        artist_name = form.artist_name.data,
        vinyl_record = form.vinyl_record.data,
        vinyl_size = form.vinyl_size.data,
        item_price = form.item_price.data,
        stock_available = form.stock_available.data,
        product_description = form.product_description.data)

        db.session.add(product)
        db.session.commit()

        print('Succesfully create new product', 'success')
        return redirect(url_for('product.create'))

    return render_template('components/create_product.html', form=form)

def get_product():
    return product