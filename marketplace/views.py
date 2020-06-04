from flask import Blueprint, render_template, session
from . import db
from .models import Product, ProductType
from .forms import LoginForm, RegisterForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #new_product = Product(artist_name = "Epic Band", album_title = "Epic Music", price = 100.01, stock = 2, vinyl_size = "7", category = ProductType.vinyl, image = "vinyl-record.jpg")
    #db.session.add(new_product)
    #db.session.commit()

    vinyls = Product.query.filter_by(category = ProductType.vinyl).limit(6).all()
    accessories = Product.query.filter_by(category = ProductType.accessory).limit(6).all()
    players = Product.query.filter_by(category = ProductType.player).limit(6).all()
    
    session['logged'] = 0

    return render_template("index.html", vinyls=vinyls, accessories=accessories, players=players)

@bp.route('/item_create')
def item_create():
    return render_template("item_create.html")

@bp.route('/item_details')
def item_details():
    return render_template("item_details.html")
    
# WORKING
@bp.route('/list')
def item_list(type = None):
    if type:
        prodlist = Product.query.filter_by(category = type).all()
    else:
        prodlist = Product.query.all()
    return render_template("item_list.html", prodlist=prodlist)

# TRIALING
@bp.route('/vinyls')
def item_list_vinyl():
    prodlist = Product.query.all()#filter_by(category = ProductType.vinyl).
    return render_template("item_list.html", prodlist=prodlist)

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
