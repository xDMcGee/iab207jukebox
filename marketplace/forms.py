#Primary Imports
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, MultipleFileField, SelectField, RadioField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, ValidationError, Regexp

#Custom Imports
from .models import ProductType, SubTypes


#Function to check the length of an input
def length_check(checkType='BSB', reqLength=6):
    message = 'Please enter a valid %d digit %s number' % (
        reqLength, checkType)

    def _length(form, field):
        l = field.data and len(str(field.data)) or 0
        if l != reqLength:
            raise ValidationError(message)

    return _length


#Login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")


#Registration form
class RegisterForm(FlaskForm):
    #Required inputs
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number = StringField('Phone number', validators=[InputRequired(), length_check(checkType='Phone', reqLength=10), Regexp('^[0-9]+$', message='Please use only the numbers 0-9')])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #Account Type input
    account_type = SelectField('Account Type', choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], validate_choice=False, id="select_user_type")

    #Optional inputs dependant on account type
    bsb = StringField("BSB", validators=[Optional(), length_check(checkType='BSB', reqLength=6), Regexp('^[0-9]+$', message='Please use only the numbers 0-9')], id="bsb_input")
    account_no = IntegerField("Account Number", validators=[Optional(), Regexp('^[0-9]+$', message='Please use only the numbers 0-9'), length_check(checkType='Account', reqLength=9)], id="account_no_input")

    # submit button
    submit = SubmitField("Register")


#Product creation form
class ProductForm(FlaskForm):
    #Query the category choices
    type_choices=ProductType.choices()
    for choice in range(len(type_choices)):
        type_choices[choice] = type_choices[choice][::-1]
    product_type = SelectField("Product Type", choices=type_choices, validate_choice=False, id="select_product_type")

    #Assign subcategory choices, these get overridden with jQuery
    sub_type_choices = SubTypes.fullchoices(SubTypes)
    product_sub_type = SelectField("Product Sub Type", choices=sub_type_choices, validate_choice=False, id="select_sub_type")

    #Standard inputs
    item_name = StringField('Product name', validators=[InputRequired()])
    item_manufacturer = StringField('Product Manufacturer', validators=[InputRequired()])
    price = IntegerField('Item price', validators=[InputRequired()])
    stock = IntegerField('Number of stock', validators=[InputRequired()])
    description = TextAreaField('Description of product', validators=[InputRequired()])

    #Image inputs
    image = FileField('Image', validators=[FileRequired(), FileAllowed({'jpg', 'png'}, message='Images only!')])

    #Submit button
    submit = SubmitField('Create')


#Filter form for browsing
class FilterForm(FlaskForm):
    sub_type_choices = SubTypes.fullchoices(SubTypes)
    product_sub_type = SelectField("", choices=sub_type_choices, validate_choice=False, id="select_sub_type")


#Simple comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post')


class OrderForm(FlaskForm):
    #Standard inputs
    street_address = StringField('Street Address', validators=[InputRequired()])
    street_address2 = StringField('Street Address 2', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state = StringField('State/Province', validators=[InputRequired()])

    #Validated number inputs
    postcode = StringField('Postcode', validators=[InputRequired(), Regexp('^[0-9]+$', message='Please use only the numbers 0-9'), length_check(checkType='Postcode', reqLength=4)])
    quantity = StringField('Quantity', validators=[InputRequired(), Regexp('^[0-9]+$', message='Please use only the numbers 0-9')])

    #Submit button
    submit = SubmitField('Order Item')
