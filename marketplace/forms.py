from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, MultipleFileField, SelectField, RadioField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, NumberRange

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

    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #Select what user account to use
    account_type = SelectField('Account Type', choices=[('Buyer','Buyer'),('Seller','Seller')], validate_choice=False, id="select_user_type")
    bsb = IntegerField("BSB", validators=[NumberRange(min=000000, max=999999, message="This is not a valid BSB"), Optional()], id="bsb_input")
    account_no = IntegerField("Account Number", validators=[NumberRange(min=000000000, max=999999999, message="This is not a valid Account Number"), Optional()], id="account_no_input")

    #submit button
    submit = SubmitField("Register")

class ProductForm(FlaskForm):

    type_choices = ProductType.choices()
    for choice in range(len(type_choices)):
        type_choices[choice] = type_choices[choice][::-1]
    product_type = SelectField("Product Type", choices=type_choices, validate_choice=False, id="select_product_type")

    sub_type_choices = SubTypes.fullchoices(SubTypes)
    product_sub_type = SelectField("Product Sub Type", choices=sub_type_choices, validate_choice=False, id="select_sub_type")

    item_name = StringField('Product name', validators=[InputRequired()])
    item_manufacturer = StringField('Product Manufacturer', validators=[InputRequired()])
    
    price = IntegerField('Item price', validators=[InputRequired()])
    stock = IntegerField('Number of stock', validators=[InputRequired()])
    description = TextAreaField('Description of product', validators=[InputRequired()])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed({'jpg', 'png'}, message = 'Images only!')])
    #image = MultipleFileField('Image of the product', [validators.regexp('^[^/\\]\.jpg$')])
    submit = SubmitField('Create')

class FilterForm(FlaskForm):
    sub_type_choices = SubTypes.fullchoices(SubTypes)
    product_sub_type = SelectField("", choices=sub_type_choices, validate_choice=False, id="select_sub_type")

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post')

class OrderForm(FlaskForm):
    address = StringField('Delivery Addresss', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    bsb = IntegerField('BSB number', validators=[InputRequired()])
    account_number = IntegerField('Account Number', validators=[InputRequired()])