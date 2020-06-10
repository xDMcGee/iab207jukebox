
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, MultipleFileField,SelectField,RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo

from .models import ProductType, SubTypes

#creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field


    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #Select what user account to use
    account_type = RadioField('Account Type', choices=[('Buyer','Buyer'),('Seller','Seller')])
    

    #submit button
    submit = SubmitField("Register")

class ProductForm(FlaskForm):
    product_type = SelectField("Product Type", choices=ProductType.choices(), coerce=int)
    product_sub_type = SelectField("Product Sub Type", choices=SubTypes.ProductSubType.VinylType.choices())

    album_title = StringField('Product name', validators=[InputRequired()])
    artist_name = StringField('Artist name', validators=[InputRequired()])
    
    price = IntegerField('Item price', validators=[InputRequired()])
    stock = IntegerField('Number of stock', validators=[InputRequired()])
    description = TextAreaField('Description of product', validators=[InputRequired()])
    #image = MultipleFileField('Image of the product', [validators.regexp('^[^/\\]\.jpg$')])
    submit = SubmitField('Create')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post')
