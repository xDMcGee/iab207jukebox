from flask import Blueprint, render_template, session
from . import db
from .models import Product
from .forms import LoginForm, RegisterForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #new_user = User(name="Poop")
    #db.session.add(new_user)
    #db.session.commit()

    #new_product = Product(artist_name = "Epic Band", album_title = "Epic Music", price = 100.01, stock = 2, vinyl_size = "7", category = "Vinyl", image = "vinyl-record.jpg")
    #db.session.add(new_product)
    #db.session.commit()

    vinyls = Product.query.filter(Product.category == "Vinyl")
    accessories = Product.query.filter(Product.category == "Accessory")
    players = Product.query.filter(Product.category == "Player")
    session['logged'] = 0

    return render_template("index.html", vinyls=vinyls, accessories=accessories, players=players)

@bp.route('/item_create')
def item_create():
    return render_template("item_create.html")

@bp.route('/item_details')
def item_details():
    return render_template("item_details.html")

@bp.route('/item_list')
def item_list():
    return render_template("item_list.html")

@bp.route('/item_order')
def item_order():
    return render_template("item_order.html")

@bp.route('/login')
def login():
    login_form = LoginForm()

    return render_template("user.html", heading = "login", form = login_form)

@bp.route('/register')
def register():
    register_form = RegisterForm()

    return render_template("user.html", form = register_form)
