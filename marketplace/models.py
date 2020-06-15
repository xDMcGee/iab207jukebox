#Primary Imports
from datetime import datetime
from flask_login import UserMixin
from aenum import Enum, skip

#Custom Imports
from . import db


#Custom class for Enum inheritance
class FormEnum(Enum):
    #Function to generate dropdown-compatible list of items
    @classmethod
    def choices(cls):
        return [(str(choice.name), choice.value) for choice in cls]


#Enum for product types
class ProductType(FormEnum):
    Vinyl = 0
    Accessory = 1
    Player = 2


#Class that contains all product subtype information
class SubTypes(FormEnum):
    #Nested class for subtypes
    class ProductSubType(Enum):
        @skip
        class VinylType(FormEnum):
            i7 = "7-Inch"
            i10 = "10-Inch"
            i12 = "12-Inch"
        @skip
        class AccessoryType(FormEnum):
            needles = "Needles"
            motors = "Motors"
            tonearms = "Tonearms"
            shelves = "Shelves"
            cleaning = "Cleaning"
        @skip
        class TableType(FormEnum):
            auto = "Automatic Tables"
            manual = "Manual Tables"

    #Function to generate list of all subtypes
    def fullchoices(self):
        self.VinylType = self.ProductSubType.VinylType
        self.AccessoryType = self.ProductSubType.AccessoryType
        self.TableType = self.ProductSubType.TableType
        return(self.VinylType.choices() + self.AccessoryType.choices() + self.TableType.choices())

    #Function to generate list of specific subtypes
    def specchoice(self, arg):
        options = {
            0 : self.ProductSubType.VinylType.choices(),
            1 : self.ProductSubType.AccessoryType.choices(),
            2 : self.ProductSubType.TableType.choices()
        }
        return(options[arg])

    #Refereneces to deeper Enum options (Required for database functionality)
    i7 = ProductSubType.VinylType.i7
    i10 = ProductSubType.VinylType.i10
    i12 = ProductSubType.VinylType.i12

    needles = ProductSubType.AccessoryType.needles
    motors = ProductSubType.AccessoryType.motors
    tonearms = ProductSubType.AccessoryType.tonearms
    shelves = ProductSubType.AccessoryType.shelves
    cleaning = ProductSubType.AccessoryType.cleaning

    auto = ProductSubType.TableType.auto
    manual = ProductSubType.TableType.manual


#User db model
class User(db.Model, UserMixin):
    __tablename__='users'

    #Primary columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_type = db.Column(db.Enum('Buyer', 'Seller', name='userType'), nullable=False)
    bsb = db.Column(db.String(6), unique=True, nullable=True)
    account_no = db.Column(db.String(9), unique=True, nullable=True)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)

    #Relationship definitions
    products = db.relationship('Product', backref='user')
    orders = db.relationship('Order',  backref="user")
    comments = db.relationship('Comment', backref='user')


#Product db model
class Product(db.Model):
    __tablename__='products'

    #Primary columns
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), index=True, nullable=False)
    item_manufacturer = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Enum(ProductType), index=True, nullable=False)
    subcategory = db.Column(db.Enum(SubTypes), index=True, nullable=False)
    image = db.Column(db.String(255), index=True) #, nullable=False)
    created_date = db.Column(db.DateTime, default = datetime.utcnow)

    #Foreign key columns
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #Relationship definitions
    comments = db.relationship('Comment', backref='product')


#Comment db model
class Comment(db.Model):
    __tablename__ ='comments'
    
    #Primary columns
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), index=True, nullable=False)
    text = db.Column(db.String(400))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    #Foreign key columns
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


#Order db model
class Order(db.Model):
    __tablename__='orders'

    #Primary columns
    order_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable = False)
    date_placed = db.Column(db.DateTime, default=datetime.utcnow)
    street_address = db.Column(db.String(50), nullable=False)
    street_address_2 = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(4), nullable=False)

    #Relationship definitions
    product = db.relationship('Product', backref='orders')

    #Foreign key columns
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))