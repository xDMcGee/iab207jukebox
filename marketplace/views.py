from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('user.html')