from flask import Blueprint, render_template
from . import db
from .models import User

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    #new_user = User(name="Poop")
    #db.session.add(new_user)
    #db.session.commit()

    users = User.query.all()
    return render_template("index.html", users=users )

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