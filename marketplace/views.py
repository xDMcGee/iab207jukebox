from flask import Blueprint, render_template
from . import db
from .models import User
from .forms import LoginForm, RegisterForm
from app import app

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #new_user = User(name="Poop")
    #db.session.add(new_user)
    #db.session.commit()
    #users = User.query.all()

    return render_template("index.html", logged=0)

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



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500 