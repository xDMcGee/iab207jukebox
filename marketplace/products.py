from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product, Comment, ProductSubType
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
        cat = dict(form.product_type.choices).get(form.product_type.data)
        subcat = dict(form.product_sub_type.choices).get(form.product_sub_type.data)

        product = Product(album_title = form.album_title.data,
        artist_name = form.artist_name.data,
        category = cat,
        subcategory = (ProductSubType.VinylType[subcat]).name,
        price = form.price.data,
        stock = form.stock.data,
        description = form.description.data,
        seller_id = 1)

        db.session.add(product)
        db.session.commit()

        print('Succesfully create new product', 'success')
        return redirect(url_for('product.create'))

    return render_template('components/create_product.html', form=form)

def get_product():
    return product