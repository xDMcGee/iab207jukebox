from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect, session
) 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm,RegisterForm

from . import db




#create a blueprint
bp = Blueprint('auth', __name__)

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
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     register_form = RegisterForm()
#     print('Method Type: ', request.method)
#     if register_form.validate_on_submit():
#         user_add = User(name=register_form.user_name.data,
#                         password_hash=generate_password_hash(register_form.confirm.data, salt_length=16),
#                         email_id=register_form.email_id.data,
#                         user_type=register_form.account_type.data)
#         db.session.add(user_add)
#         db.session.commit()
#         print('Successfully created account!', 'Success')
#         #return redirect(url_for('user'))

#     return render_template("user.html", form=register_form)

@bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    if (register.validate_on_submit() == True):
        user_name = register.user_name.data
        password = register.password.data
        email = register.email_id.data
        user_type = register.account_type.data

        u1 = User.query.filter_by(name=user_name).first()
        if u1:
            flash('User name already exist, please login')
            return redirect(url_for('auth.login'))
        password = generate_password_hash(password)
        new_user = User(name=user_name, password_hash=password, email_id = email, user_type = user_type)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index.html'))

    else:
        return render_template('user.html', form = register, heading='Register')



# this is the hint for a login function
# @bp.route('/login', methods=['GET', 'POST'])
# def authenticate(): #view function
#     print('In Login View function')
#     login_form = LoginForm()
#     error=None
#     if(login_form.validate_on_submit()==True):
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         u1 = User.query.filter_by(name=user_name).first()
#         if u1 is None:
#             error='Incorrect user name'
#         elif not check_password_hash(u1.password_hash, password): # takes the hash and password
#             error='Incorrect password'
#         if error is None:
#             login_user(u1)
#             nextp = request.args.get('next') #this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
