from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from .models import Product, Comment, ProductType, SubTypes
from .forms  import ProductForm
from . import db

import os

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/<id>')
def show(id):
    product = Product.query.filter_by(id=id).first()
    return render_template('show.html', product = product)

@bp.route('/create', methods=['GET','POST'])
def create():
    print('Method type', request.method)
    form = ProductForm()
    if form.validate_on_submit():
        cat = dict(form.product_type.choices).get(int(form.product_type.data))

        img_file = form.image.data
        filename = str(img_file.filename).replace(" ", "")

        BASE_PATH = os.path.dirname(__file__)

        oldId = Product.query.order_by(Product.id.desc()).first()
        oldId = oldId.id

        dir_path = os.path.join(BASE_PATH, 'static/img/' + str(oldId + 1))
        os.makedirs(dir_path)

        upload_path = os.path.join(BASE_PATH, 'static/img/' + str(oldId + 1), secure_filename(filename))
        img_file.save(upload_path)

        product = Product(
        item_name = form.item_name.data,
        item_manufacturer = form.item_manufacturer.data,
        price = form.price.data,
        stock = form.stock.data,
        description = form.description.data,
        category = ProductType[cat],
        subcategory = SubTypes[form.product_sub_type.data],
        image = filename,
        seller_id = 1)

        db.session.add(product)
        db.session.commit()

        print('Succesfully create new product', 'success')
        return redirect(url_for('product.create'))

    return render_template('components/create_product.html', form=form)

@bp.route('/_get_subtypes/')
def _get_subtypes():
    product_type = request.args.get('pt', 0, type=int)
    sub_type = SubTypes.specchoice(SubTypes, product_type)
    return jsonify(sub_type)

# def get_product():
#     return product