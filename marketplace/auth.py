from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from sqlalchemy import and_, or_

from . import db
from .forms import LoginForm, RegisterForm
from .models import User

#create a blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

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

        uTest = User.query.filter(or_(User.name == register_form.user_name.data, User.email_id == register_form.email_id.data, User.phone_number == register_form.phone_number.data)).first()
        if uTest:
            flash('A User with this information already exists, please try again')
            return redirect(url_for('auth.register'))

        if (register_form.account_type.data == "Buyer"):
            bsb = None
            account_no = None
        else:
            bsb = register_form.bsb.data
            account_no = register_form.account_no.data
            accTest = User.query.filter(or_(User.bsb == str(register_form.bsb.data), User.account_no == str(register_form.account_no.data))).first()
            if accTest:
                flash('A User with this information already exists, please try again')
                return redirect(url_for('auth.register'))

        user_add = User(name=register_form.user_name.data,
                        password_hash=generate_password_hash(register_form.confirm.data, salt_length=16),
                        email_id=register_form.email_id.data,
                        user_type=register_form.account_type.data,
                        bsb=bsb,
                        account_no=account_no,
                        phone_number=register_form.phone_number.data)

        db.session.add(user_add)
        db.session.commit()
        print('Successfully created account!', 'Success')
        return redirect(url_for('auth.authenticate'))

    return render_template("user.html", form=register_form, heading='Register')

@bp.route('/signout')
def signout():
    logout_user()
    return 'Logout Successful'