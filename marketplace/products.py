#Primary Imports
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, current_app, flash
from flask_login import current_user
from sqlalchemy import and_
from werkzeug.utils import secure_filename
from datetime import datetime
import os

#Custom Imports
from .models import Product, Comment, ProductType, SubTypes, Order
from .forms import ProductForm, CommentForm, OrderForm
from . import db

#Blueprint definition
bp = Blueprint('product', __name__, url_prefix='/products')


#Specific Product route
@bp.route('/<id>')
def show(id):
    #Query product using id
    product = Product.query.filter_by(id=id).first()

    #Throw a 404 if product does not exist
    if product is None:
        abort(404)

    #Find similar products
    similarProducts = Product.query.filter(and_(Product.category == product.category, Product.id != product.id)).limit(4).all()

    #Check if the user has purchased this item - required to leave comments
    hasBought = None
    if current_user.is_authenticated:
        if current_user.user_type == "Buyer":
            hasBought = Order.query.filter(and_(Order.product_id == id, Order.buyer_id == current_user.id)).all()
            
    cform = CommentForm()
    return render_template('show.html', product=product, hasBought = hasBought, similarProducts = similarProducts, form=cform)


#Hidden route for creating coments
@bp.route('/<id>/comment', methods=['GET', 'POST'])
def comment(id):
    #Find the product for the comment
    product = Product.query.filter_by(id=id).first()

    #Form generation and submission check
    cform = CommentForm()
    if cform.validate_on_submit():

        #Create comment object for db
        comment = Comment(
            user_name=current_user.name,
            text=cform.text.data,
            product_id=product.id,
            user_id=current_user.id
        )

        #Commit object to db
        db.session.add(comment)
        db.session.commit()
        #Server-side note
        print('Your comment has been added', 'success')
    
    #Reload the products page w/ new comments
    return redirect(url_for('.show', id=id))


#Item creation route
@bp.route('/create', methods=['GET', 'POST'])
def create():
    #Authentication check
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    print('Method type', request.method)

    #Form generation and submission
    form = ProductForm()
    if form.validate_on_submit():

        #Get the category name by comparing the selected result with a dictionary of available results
        cat = dict(form.product_type.choices).get(int(form.product_type.data))

        #Get the image and remove spaces from filename
        img_file = form.image.data
        filename = str(img_file.filename).replace(" ", "")

        #Create product object for db
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

        #Commit object to db
        db.session.add(product)
        db.session.commit()

        #Get file path
        BASE_PATH = os.path.dirname(__file__)

        #Get id for latest product
        Id = Product.query.order_by(Product.id.desc()).first()
        Id = Id.id

        #Use id to make new image subfolder
        dir_path = os.path.join(BASE_PATH, 'static/img/' + str(Id))
        os.makedirs(dir_path, exist_ok=True)

        #Upload to subfolder
        upload_path = os.path.join(BASE_PATH, 'static/img/' + str(Id), secure_filename(filename))
        img_file.save(upload_path)

        #Server-side message and redirect to new product page
        print('Succesfully create new product', 'success')
        return redirect(url_for('product.show', id = Id))

    return render_template('components/create_product.html', form=form)


#Route for sellers listings
@bp.route('/mine')
def mine():
    #Authentication checks
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    #Query the products for the current user
    prodlist = Product.query.filter_by(seller_id = current_user.id).all()
    header = "My Products:"

    return render_template("item_list.html", prodlist = prodlist, arg = None, header = header, editMode = True)


#Hidden product deletion route
@bp.route('/_delete_product/')
def _delete_product():
    #Authentication check
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif not current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    #Get the product id and query the product
    id = request.args.get('id', 0, type=int)
    prod = Product.query.filter_by(id = id).first()

    #Check to make sure request is coming from the seller
    if prod.seller_id == current_user.id:
        #Delete the product
        Product.query.filter_by(id = id).delete()
        db.session.commit()
    else:
        #Return failure if unauthorised and redirect to login
        print('Not authorised for this delete action', 'failure')
        return current_app.login_manager.unauthorized()

    #Server-side message
    print('Deleting product with ID:' + str(id))
    
    return redirect(url_for('.mine'))


#Buyer order route
@bp.route('/order/<id>', methods=['GET', 'POST'])
def order(id):
    #Authentication checks
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()

    #Query product and similar products
    product = Product.query.filter_by(id=id).first()
    similarProducts = Product.query.filter(and_(Product.category == product.category, Product.id != product.id)).limit(4).all()

    #Form generation and submissio
    order_form = OrderForm()
    if order_form.validate_on_submit():

        #Stock and quantity check
        if int(order_form.quantity.data) > product.stock:
            flash('Cannot purchase more than the available stock')
            return redirect(url_for('product.order', id = id))

        if order_form.validate_on_submit():

            #Create object for db
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

            #Deduct quantity from stock and commit
            product.stock -= int(order_form.quantity.data)
            db.session.add(order)
            db.session.commit()

            return redirect(url_for('main.order_list'))

    return render_template("item_order.html", product = product, similarProducts = similarProducts, form = order_form)


#Hidden route for jQuery dropdown methods
@bp.route('/_get_subtypes/')
def _get_subtypes():
    #Define the product type from URL param
    product_type = request.args.get('pt', 0, type=int)

    #Request function from enum and return
    sub_type = SubTypes.specchoice(SubTypes, product_type)
    return jsonify(sub_type)
