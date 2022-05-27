from sqlalchemy import JSON
from app import db
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Item(db.Model):
    __tablename__="Items"
    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String(100))
    data=db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    


