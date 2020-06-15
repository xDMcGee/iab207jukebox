#import flask - from the package import class
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os

db=SQLAlchemy()

from .models import User, Product, ProductType, SubTypes

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    #the folder to store images
    UPLOAD_FOLDER = '/static/img'
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///marketplace.sqlite'
    app.config.from_mapping(
        #Flask SQLAlchemy settings
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
    )
    #initialize db with flask app
    db.init_app(app)

    ctx=app.app_context()
    ctx.push()
    db.create_all()

    bootstrap = Bootstrap(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    #from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.authenticate'))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import products
    app.register_blueprint(products.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    app.jinja_env.globals.update(ProductType=ProductType)
    app.jinja_env.globals.update(SubTypes=SubTypes)

    #Error handling returns set pages
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500 

        
    return app



