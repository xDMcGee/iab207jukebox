from . import db

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)