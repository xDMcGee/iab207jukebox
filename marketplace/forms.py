
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, MultipleFileField,SelectField,RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo


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
    account_type = RadioField('Account Type', choices=[('0','Buyer'),('1','Seller')])
    
    
    #submit button
    submit = SubmitField("Register")

class ProductForm(FlaskForm):
    album_title = StringField('Product name', validators=[InputRequired()])
    artist_name = StringField('Artist name', validators=[InputRequired()])
    vinyl_record = StringField('Vinyl record', validators=[InputRequired()])
    vinyl_size = IntegerField('Vinyl size', validators=[InputRequired()])
    item_price = IntegerField('Item price', validators=[InputRequired()])
    stock_available = IntegerField('Number of stock', validators=[InputRequired()])
    product_description = TextAreaField('Description of product', validators=[InputRequired()])
    #image = MultipleFileField('Image of the product', [validators.regexp('^[^/\\]\.jpg$')])
    submit = SubmitField('Create')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post')
