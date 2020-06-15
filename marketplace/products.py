from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Product, Comment, ProductType, SubTypes, Order
from .forms import ProductForm, CommentForm, OrderForm
from . import db
from flask_login import current_user
from sqlalchemy import and_

import os

bp = Blueprint('product', __name__, url_prefix='/products')


@bp.route('/<id>')
def show(id):
    product = Product.query.filter_by(id=id).first()
    hasBought = None
    if product is None:
        abort(404)

    similarProducts = Product.query.filter(and_(Product.category == product.category, Product.id != product.id)).limit(6).all()

    if current_user.is_authenticated:
        if current_user.user_type == "Buyer":
            hasBought = Order.query.filter(and_(Order.product_id == id, Order.buyer_id == current_user.id)).all()
            
            
    # Reformatting the date to be user-readable
    cform = CommentForm()
    return render_template('show.html', product=product, hasBought = hasBought, similarProducts = similarProducts, form=cform)


@bp.route('/<id>/comment', methods=['GET', 'POST'])
def comment(id):
    product = Product.query.filter_by(id=id).first()
    cform = CommentForm()
    if cform.validate_on_submit():
        comment = Comment(
            user_name=current_user.name,
            text=cform.text.data,
            product_id=product.id,
            user_id=current_user.id
        )

        db.session.add(comment)
        db.session.commit()
        print('Your comment has been added', 'success')
    return redirect(url_for('.show', id=id))


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    print('Method type', request.method)
    form = ProductForm()
    if form.validate_on_submit():
        cat = dict(form.product_type.choices).get(int(form.product_type.data))

        img_file = form.image.data
        filename = str(img_file.filename).replace(" ", "")

        BASE_PATH = os.path.dirname(__file__)

        oldId = Product.query.order_by(Product.id.desc()).first()
        if not (oldId is None):
            oldId = oldId.id
        else:
            oldId = 0

        dir_path = os.path.join(BASE_PATH, 'static/img/' + str(oldId + 1))
        os.makedirs(dir_path, exist_ok=True)

        upload_path = os.path.join(
            BASE_PATH, 'static/img/' + str(oldId + 1), secure_filename(filename))
        img_file.save(upload_path)

        product = Product(
            item_name=form.item_name.data,
            item_manufacturer=form.item_manufacturer.data,
            price=form.price.data,
            stock=form.stock.data,
            description=form.description.data,
            category=ProductType[cat],
            subcategory=SubTypes[form.product_sub_type.data],
            image=filename,
            seller_id=1)

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


@bp.route('/order/<id>', methods=['GET', 'POST'])
def order(id):
    product = Product.query.filter_by(id=id).first()
    similarProducts = Product.query.filter(and_(Product.category == product.category, Product.id != product.id)).limit(6).all()
    order_form = OrderForm()

    if order_form.validate_on_submit():
        if order.quantity > Product.stock:
            print('Cannot purchase more than the available stock')
            return redirect(url_for('product.order'))

        if order_form.validate_on_submit():
            order = Order(
                address = order_form.address.data,
                product_id = product.id,
                buyer_id = current_user.id,
                seller_id = product.seller_id,
                quantity = order_form.quantity.data
            )
    return render_template("item_order.html", product = product, similarProducts = similarProducts)

