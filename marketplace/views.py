from flask import Blueprint, render_template
from os import listdir

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return listdir("/templates")