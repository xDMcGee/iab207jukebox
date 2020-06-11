from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from . import db
from .models import Product, ProductType, User
from .forms import LoginForm, RegisterForm, ProductForm, SearchForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required,logout_user
# from products import show, create
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    users = User.query.all()
    vinyls = Product.query.filter_by(category=ProductType['Vinyl']).limit(6).all()
    accessories = Product.query.filter_by(category=ProductType['Accessory']).limit(6).all()
    players = Product.query.filter_by(category=ProductType['Player']).limit(6).all()

    # if session['user'] == None:
    session['logged'] = 0
    
    return render_template("index.html", vinyls=vinyls, accessories=accessories, players=players, users=users)

@bp.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_input = form.query.data
        print(search_input)
        item_create()
    return render_template("search_bar.html", searchForm = form)

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
    prType = request.args.get('type')
    prSearch = request.args.get('search')
    if not (prType is None):
        prodlist = Product.query.filter_by(category=ProductType[prType]).all()
    else:
        if not (prSearch is None):
            prodlist = Product.query.filter_by(name=prSearch).all()
        else:
            prodlist = Product.query.all()
    return render_template("item_list.html", prodlist=prodlist)


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
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
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
                        user_type=register_form.account_type.data)
        db.session.add(user_add)
        db.session.commit()
        print('Successfully created account!', 'Success')
        #return redirect(url_for('user'))

    return render_template("user.html", form=register_form)

@bp.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', none)
    return 'Session has been clear'