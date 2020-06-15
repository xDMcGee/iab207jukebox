#Primary Imports
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from sqlalchemy import and_, or_

#Custom Imports
from . import db
from .forms import LoginForm, RegisterForm
from .models import User

#Bluepring definition
bp = Blueprint('auth', __name__, url_prefix='/auth')


#Login route
@bp.route('/login', methods=['GET', 'POST'])
def authenticate():
    error=None

    #Form creation and submission
    login_form = LoginForm()
    if login_form.validate_on_submit():

        #Define variables
        user_name = login_form.user_name.data
        password = login_form.password.data

        #Query if user exits
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error = 'Incorrect user name'
        #Compare password with hash
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'
        #Proceed if successful
        if error is None:
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            flash(error)

    return render_template('user.html', form=login_form, heading='Login')


#Registration route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    print('Method Type: ', request.method)

    #Form creation and submission
    register_form = RegisterForm()
    if register_form.validate_on_submit():

        #Check if user exists with any unique info
        uTest = User.query.filter(or_(User.name == register_form.user_name.data, User.email_id == register_form.email_id.data, User.phone_number == register_form.phone_number.data)).first()
        if uTest:
            flash('A User with this information already exists, please try again')
            return redirect(url_for('auth.register'))

        #Set variables to None if buyer selected
        if (register_form.account_type.data == "Buyer"):
            bsb = None
            account_no = None
        else:
            #Define bank info
            bsb = register_form.bsb.data
            account_no = register_form.account_no.data

            #Check if account with bank info exists
            accTest = User.query.filter(or_(User.bsb == str(register_form.bsb.data), User.account_no == str(register_form.account_no.data))).first()
            if accTest:
                flash('A User with this information already exists, please try again')
                return redirect(url_for('auth.register'))

        #Generate db object
        user_add = User(name=register_form.user_name.data,
                        password_hash=generate_password_hash(register_form.confirm.data, salt_length=16),
                        email_id=register_form.email_id.data,
                        user_type=register_form.account_type.data,
                        bsb=bsb,
                        account_no=account_no,
                        phone_number=register_form.phone_number.data)

        #Add and commit to db
        db.session.add(user_add)
        db.session.commit()

        #Server-side notes
        print('Successfully created account!', 'Success')
        return redirect(url_for('auth.authenticate'))

    return render_template("user.html", form=register_form, heading='Register')


#Simple signout route
@bp.route('/signout')
def signout():
    logout_user()
    return 'Logout Successful'