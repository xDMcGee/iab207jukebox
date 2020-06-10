from . import db
from datetime import datetime
import enum

from aenum import Enum, skip

class User(db.Model):
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

class FormEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)

class ProductType(FormEnum):
    Vinyl = 0
    Player = 1
    Accessory = 2

class SubTypes:
    class ProductSubType(Enum):
        @skip
        class VinylType(FormEnum):
            i7 = 0
            i10 = 1
            i12 = 2
        @skip
        class AccessoryType(Enum):
            needles = "Needles"
            motors = "Motors"
            tonearms = "Tonearms"
            shelves = "Shelves"
            cleaning = "Cleaning"
        @skip
        class TableType(Enum):
            auto = "Automatic Tables"
            manual = "Manual Tables"

    i7 = ProductSubType.VinylType.i7
    i10 = ProductSubType.VinylType.i10
    i12 = ProductSubType.VinylType.i12

    def setValue(self, subType):
        self.value = SubType

class Product(db.Model):
    __tablename__='products'

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(255), index=True, nullable=False)
    album_title = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    subcategory = db.Column(db.Enum(SubTypes.ProductSubType), index=True, nullable=False)
    category = db.Column(db.Enum(ProductType), index=True, nullable=False)
    image = db.Column(db.String(255), index=True, nullable=False)
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