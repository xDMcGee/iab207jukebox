from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template("index.html")

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