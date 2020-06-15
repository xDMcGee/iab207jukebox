from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, MultipleFileField, SelectField, RadioField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, ValidationError, Regexp

from .models import ProductType, SubTypes

# creates the login information


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")


def length_check(checkType='BSB', reqLength=6):
    message = 'Please enter a valid %d digit %s number' % (
        reqLength, checkType)

    def _length(form, field):
        l = field.data and len(str(field.data)) or 0
        if l != reqLength:
            raise ValidationError(message)

    return _length

# this is the registration form


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number = StringField('Phone number', validators=[InputRequired(), length_check(checkType='Phone', reqLength=10), Regexp('^[0-9]+$', message='Please use only the numbers 0-9')])

    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm=PasswordField("Confirm Password")

    # Select what user account to use
    account_type=SelectField('Account Type', choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], validate_choice=False, id="select_user_type")
    bsb=StringField("BSB", validators=[Optional(), length_check(checkType='BSB', reqLength=6), Regexp('^[0-9]+$', message='Please use only the numbers 0-9')], id="bsb_input")
    account_no=StringField("Account Number", validators=[Optional(), Regexp('^[0-9]+$', message='Please use only the numbers 0-9'), length_check(checkType='Account', reqLength=9)], id="account_no_input")

    # submit button
    submit=SubmitField("Register")

class ProductForm(FlaskForm):
    type_choices=ProductType.choices()
    for choice in range(len(type_choices)):
        type_choices[choice]=type_choices[choice][::-1]
    product_type=SelectField("Product Type", choices=type_choices,
                             validate_choice=False, id="select_product_type")

    sub_type_choices=SubTypes.fullchoices(SubTypes)
    product_sub_type=SelectField(
        "Product Sub Type", choices=sub_type_choices, validate_choice=False, id="select_sub_type")

    item_name=StringField('Product name', validators=[InputRequired()])
    item_manufacturer=StringField(
        'Product Manufacturer', validators=[InputRequired()])

    price=IntegerField('Item price', validators=[InputRequired()])
    stock=IntegerField('Number of stock', validators=[InputRequired()])
    description=TextAreaField('Description of product',
                              validators=[InputRequired()])
    image=FileField('Image', validators=[
        FileRequired(),
        FileAllowed({'jpg', 'png'}, message='Images only!')])
    # image = MultipleFileField('Image of the product', [validators.regexp('^[^/\\]\.jpg$')])
    submit=SubmitField('Create')

class FilterForm(FlaskForm):
    sub_type_choices=SubTypes.fullchoices(SubTypes)
    product_sub_type=SelectField("", choices=sub_type_choices, validate_choice=False, id="select_sub_type")

class CommentForm(FlaskForm):
    text=TextAreaField('Comment', validators=[InputRequired()])
    submit=SubmitField('Post')

class OrderForm(FlaskForm):
    street_address=StringField('Street Address', validators=[InputRequired()])
    street_address2=StringField('Street Address 2', validators=[InputRequired()])
    city=StringField('City', validators=[InputRequired()])
    state=StringField('State/Province', validators=[InputRequired()])
    postcode=IntegerField('Postcode', validators=[InputRequired(),
                                                length_check(checkType='Postcode', reqLength=4)])
    quantity=IntegerField('Quantity', validators=[InputRequired()])
    submit=SubmitField('Order Item')
