from . import db
from datetime import datetime
from flask_login import UserMixin

from aenum import Enum, skip

class User(db.Model, UserMixin):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_type = db.Column(db.Enum('Buyer', 'Seller', name='userType'), nullable=False)
    bsb = db.Column(db.String(6), unique=True)
    account_no = db.Column(db.String(9), unique=True)

    products = db.relationship('Product', backref='user')

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class FormEnum(Enum):
    @classmethod
    def choices(cls):
        return [(str(choice.name), choice.value) for choice in cls]

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

class Product(db.Model):
    __tablename__='products'

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(255), index=True, nullable=False)
    album_title = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    subcategory = db.Column(db.Enum(SubTypes), index=True, nullable=False)
    category = db.Column(db.Enum(ProductType), index=True, nullable=False)
    image = db.Column(db.String(255), index=True) #, nullable=False)
    created_date = db.Column(db.DateTime, default = datetime.utcnow)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comment(db.Model):
    __tablename__ ='comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    comment_text = db.Column(db.String(400))
    create_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Order(db.Model):
    __tablename__='orders'

    order_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date_placed = db.Column(db.DateTime, default=datetime.now())

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))