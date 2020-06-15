from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, and_

from . import db
from .models import Product, ProductType, User, SubTypes, Order
from .forms import LoginForm, RegisterForm, ProductForm, FilterForm

bp = Blueprint('main', __name__)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    term = request.args.get('search')
    return redirect(url_for('.item_list', search = term))

@bp.route('/')
def index():
    users = User.query.all()
    vinyls = Product.query.filter_by(category=ProductType['Vinyl']).order_by(Product.created_date.desc()).limit(6).all()
    accessories = Product.query.filter_by(category=ProductType['Accessory']).order_by(Product.created_date.desc()).limit(6).all()
    players = Product.query.filter_by(category=ProductType['Player']).order_by(Product.created_date.desc()).limit(6).all()

    return render_template("index.html", vinyls=vinyls, accessories=accessories, players=players, users=users)

@bp.route('/list')
def item_list():
    
    filterForm = FilterForm()
    prType = request.args.get('type')
    prSubType = request.args.get('subtype')
    prSearch = request.args.get('search')

    if not (prType is None):
        if not (prSubType is None):
            prodlist = Product.query.filter(and_(Product.category == ProductType[prType], Product.subcategory == SubTypes[prSubType])).all()
        else:
            prodlist = Product.query.filter_by(category = ProductType[prType]).all()
        return render_template("item_list.html", prodlist = prodlist, arg = ProductType[prType].value, filterForm = filterForm, header = str(prType) + " Collection:")
    elif not (prSearch is None):
        prodlist = Product.query.filter(or_(Product.item_name.ilike('%' + prSearch + '%'), Product.item_manufacturer.ilike('%' + prSearch + '%'))).all()
        return render_template("item_list.html", prodlist = prodlist, arg = None, header = "Searching for " + str(prSearch) + ":")
    else:
        prodlist = Product.query.all()
        header = "Products:"
    return render_template("item_list.html", prodlist = prodlist, arg = None, header = header, editMode = False)


@bp.route('/MyOrders')
def order_list():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    elif current_user.user_type == "Seller":
        return current_app.login_manager.unauthorized()
    
    prodlist = Product.query.filter(and_(Product.id == Order.product_id, Order.buyer_id == current_user.id))
    header = "Your orders:"
    return render_template("item_list.html", prodlist = prodlist, arg = None, header = header, editMode = False)
