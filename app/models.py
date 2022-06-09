import base64
import os
import random
from sqlalchemy import JSON, null
from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(UserMixin,db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    api_key=db.Column(db.String(128),unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_hash_key(self):
        self.api_key=base64.b64encode(os.urandom(43)).decode('utf-8')
        db.session.commit()
    def delete_key(self):
        self.api_key=None
        db.session.commit()

   
@login.request_loader
def load_user_from_request(request):
    api_key=request.headers.get('Authorization')
    if api_key:
        #api_key = api_key.replace('Basic ', '', 1)
        #try:
        #api_key = base64.b64decode(api_key)
        #except TypeError:
        #    pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

@login.user_loader
def load_user(usr_id):
    return User.query.get(int(usr_id))

class Item(db.Model):
    __tablename__="Items"
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))



