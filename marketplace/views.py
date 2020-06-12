from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from . import db
from .models import Product, ProductType, User, SubTypes
from .forms import LoginForm, RegisterForm, ProductForm, FilterForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required,logout_user
from sqlalchemy import or_, and_
# from products import show, create
bp = Blueprint('main', __name__)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    term = request.args.get('search')
    return redirect(url_for('.item_list', search = term))

@bp.route('/')
def index():
    users = User.query.all()
    vinyls = Product.query.filter_by(category=ProductType['Vinyl']).limit(6).all()
    accessories = Product.query.filter_by(category=ProductType['Accessory']).limit(6).all()
    players = Product.query.filter_by(category=ProductType['Player']).limit(6).all()

    # if session['user'] == None:
    session['logged'] = 0

    return render_template("index.html", vinyls=vinyls, accessories=accessories, players=players, users=users)

@bp.route('/item_create', methods=['GET', 'POST'])
def item_create():
    create_form = ProductForm()
    print('Method Type: ', request.method)

    if create_form.validate_on_submit():
        print('Successfully created product!', 'Success')

    return render_template("item_create.html", form=create_form)


@bp.route('/item_details')
def item_details():
    return render_template("item_details.html")


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
        return render_template("item_list.html", prodlist = prodlist, arg = ProductType[prType].value, filterForm = filterForm)
    elif not (prSearch is None):
        prodlist = Product.query.filter(or_(Product.album_title.ilike('%' + prSearch + '%'), Product.artist_name.ilike('%' + prSearch + '%'))).all()
        return render_template("item_list.html", prodlist = prodlist, arg = None)
    else:
        prodlist = Product.query.all()
    return render_template("item_list.html", prodlist = prodlist, arg = None)


@bp.route('/item_order')
def item_order():
    return render_template("item_order.html")

@bp.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', none)
    return 'Session has been clear'