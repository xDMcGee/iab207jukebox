from . import db
from datetime import now

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

class Product(db.Model):
    __tablename__='products'

    productType = db.Enum('Vinyl', 'Player', 'Accessory', name="productType")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(productType, index=True, nullable=False)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comment(db.model):
    __tablename__ ='comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    comment_text = db.Column(db.String(400))
    create_at = db.Column(db.DateTime, default=datetime.now())

class Order(db.model):
    __tablename__='orders'

    order_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date_placed = db.Column(db.DateTime, default=datetime.now())


    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))