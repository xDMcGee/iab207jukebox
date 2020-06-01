from . import db

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(255), index=True, unique=True, nullable=False)
    user_type = db.Column(db.Enum('Buyer', 'Seller', name='userType'), nullable=False)
    bsb = db.Column(db.Integer(6), unique=True)
    account_no = db.Column(db.Integer(6), unique=True)

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class Product(db.Model):
    __tablename__='products'

    productType = db.Enum('Vinyl', 'Player', 'Accessory', name="productType")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    name = db.Column(productType, index=True, nullable=False)