from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, current_app, flash
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

    hasBought = None
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

        product = Product(
            item_name=form.item_name.data,
            item_manufacturer=form.item_manufacturer.data,
            price=form.price.data,
            stock=form.stock.data,
            description=form.description.data,
            category=ProductType[cat],
            subcategory=SubTypes[form.product_sub_type.data],
            image=filename,
            seller_id=current_user.id)

        db.session.add(product)
        db.session.commit()

        Id = Product.query.order_by(Product.id.desc()).first()
        Id = Id.id

        dir_path = os.path.join(BASE_PATH, 'static/img/' + str(Id))
        os.makedirs(dir_path, exist_ok=True)

        upload_path = os.path.join(BASE_PATH, 'static/img/' + str(Id), secure_filename(filename))
        img_file.save(upload_path)

        print('Succesfully create new product', 'success')
        return redirect(url_for('product.show', id = Id))

    return render_template('components/create_product.html', form=form)


@bp.route('/mine')
def mine():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    prodlist = Product.query.filter_by(seller_id = current_user.id).all()
    header = "My Products:"
    return render_template("item_list.html", prodlist = prodlist, arg = None, header = header, editMode = True)

@bp.route('/_delete_product/')
def _delete_product():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    id = request.args.get('id', 0, type=int)

    prod = Product.query.filter_by(id = id).first()

    if prod.seller_id == current_user.id:
        Product.query.filter_by(id = id).delete()
        db.session.commit()
    else:
        print('Not authorised for this delete action')
        return current_app.login_manager.unauthorized()

    print('Deleting product with ID:' + str(id))
    
    return redirect(url_for('.mine'))


@bp.route('/order/<id>', methods=['GET', 'POST'])
def order(id):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    product = Product.query.filter_by(id=id).first()
    similarProducts = Product.query.filter(and_(Product.category == product.category, Product.id != product.id)).limit(6).all()
    order_form = OrderForm()

    if order_form.validate_on_submit():
        if order_form.quantity.data > product.stock:
            flash('Cannot purchase more than the available stock')
            return redirect(url_for('product.order', id = id))

        if order_form.quantity.data == 0:
            flash('Product is out of stock')
            return redirect(url_for('product.order', id = id))

        if order_form.validate_on_submit():
            order = Order(
                street_address = order_form.street_address.data,
                street_address_2 = order_form.street_address2.data,
                city = order_form.city.data,
                state = order_form.state.data,
                postcode = order_form.postcode.data,
                product_id = product.id,
                buyer_id = current_user.id,
                quantity = order_form.quantity.data
            )
            product.stock -= order_form.quantity.data
            db.session.add(order)
            db.session.commit()

            # return render_template("")
    return render_template("item_order.html", product = product, similarProducts = similarProducts, form = order_form)


@bp.route('/_get_subtypes/')
def _get_subtypes():
    product_type = request.args.get('pt', 0, type=int)
    sub_type = SubTypes.specchoice(SubTypes, product_type)
    return jsonify(sub_type)
