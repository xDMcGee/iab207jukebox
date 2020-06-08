from flask import Blueprint, render_template, session, request, redirect, url_for
from werkzeug.security import generate_password_hash
from . import db
from .models import Product, ProductType, User
from .forms import LoginForm, RegisterForm, ProductForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #new_product = Product(artist_name = "Epic Band", album_title = "Epic Music", price = 100.01, stock = 2, vinyl_size = "7", category = ProductType.vinyl, image = "vinyl-record.jpg")
    # db.session.add(new_product)
    # db.session.commit()

    users = User.query.all()
    vinyls = Product.query.filter_by(category=ProductType.vinyl).limit(6).all()
    accessories = Product.query.filter_by(
        category=ProductType.accessory).limit(6).all()
    players = Product.query.filter_by(
        category=ProductType.player).limit(6).all()

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
    prType = request.args.get('type')
    if not (prType is None):
        prodlist = Product.query.filter_by(category=ProductType(prType)).all()
    else:
        prodlist = Product.query.all()
    return render_template("item_list.html", prodlist=prodlist)


@bp.route('/item_order')
def item_order():
    return render_template("item_order.html")


@bp.route('/login')
def login():
    login_form = LoginForm()

    return render_template("user.html", heading="login", form=login_form)


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
