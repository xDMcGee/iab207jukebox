from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from . import db
from .models import Product, ProductType, User, SubTypes
from .forms import LoginForm, RegisterForm, ProductForm, FilterForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user
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

@bp.route('/login', methods=['GET', 'POST'])
def authenticate(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    print('Method Type: ', request.method)
    if register_form.validate_on_submit():
        user_add = User(name=register_form.user_name.data,
                        password_hash=generate_password_hash(register_form.confirm.data, salt_length=16),
                        email_id=register_form.email_id.data,
                        user_type=register_form.account_type.data,
                        bsb=register_form.bsb.data,
                        account_no=register_form.account_no.data)
        db.session.add(user_add)
        db.session.commit()
        print('Successfully created account!', 'Success')
        #return redirect(url_for('user'))

    return render_template("user.html", form=register_form)

@bp.route('/signout')
def signout():
    logout_user()
    return 'Logout Successful'