from . import db
from datetime import datetime
import enum

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_type = db.Column(db.Enum('Buyer', 'Seller', name='userType'), nullable=False)
    bsb = db.Column(db.String(6), unique=True)
    account_no = db.Column(db.String(9), unique=True)

    #products = db.relationship('Product', backref='user')

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class ProductType(enum.Enum):
    vinyl = "Vinyl"
    player = "Player"
    accessory = "Accessory"

class Product(db.Model):
    __tablename__='products'

    vinylSizing = db.Enum('7', '10', '12', name="vinylSize")

    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(255), index=True, nullable=False)
    album_title = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    vinyl_size = db.Column(vinylSizing, index=True, nullable=False)
    category = db.Column(db.Enum(ProductType), index=True, nullable=False)
    image = db.Column(db.String(255), index=True, nullable=False)

    def __repr__(self):
        return "<Name: {}, category: {}>".format(self.artist_name, self.category)

    #seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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