import base64
import json
from urllib import response
import flask
from flask_login import current_user, login_required,login_user, logout_user
from app import app,db
from app.models import Item,User
from flask import redirect, render_template,jsonify, request


@app.route('/',methods=["POST", "GET","DELETE"])
@login_required
def index():
    u=current_user
    if request.method=="POST":
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        data=request_data['data']
        i=Item(data=data,user=u)
        db.session.add(i)
        db.session.commit()
        resp=flask.make_response("data saved successfully")
        resp.headers['id']=i.id
        return resp
    elif request.method=="GET":
        cols = ['id', 'data']
        data = Item.query.filter_by(user_id=u.id)
        result = [{col: getattr(d, col) for col in cols} for d in data]
        return jsonify(result)
    else:
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        Item.query.filter(Item.id==request_data).delete()
        db.session.commit()
        return jsonify(["item deleted"])


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/login')
    else:
        if request.method=="POST":
            request_data=request.data
            request_data=json.loads(request_data.decode("utf-8"))
            username=request_data['username']
            email=request_data['email']
            password=request_data['password']
            user = User.query.filter_by(username=username).first()
            user1 = User.query.filter_by(email=email).first()
            if user is  None:
                if user1 is None:
                    u=User(username=username,email=email)
                    u.set_password(password)
                    db.session.add(u)
                    db.session.commit()
                    return 'register success'
                else:
                    return 'Please use a different email address.'
            else:
                return 'Please use a different username.'
        
@app.route('/login',methods=['GET','POST'])
def login():
    active_user=current_user
    if request.method=="POST": 
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        
        username=request_data['username']
        password=request_data['password']
        user =User.query.filter((User.username==username)|(User.email==username)).first()
        if user is None or not user.check_password(password):
            return 'wrong username or password' 
        login_user(user,force=True)
        user.generate_hash_key()
        print(current_user.is_authenticated)
        resp=flask.make_response("login success")
        resp.headers['api-key']=user.api_key
        print(current_user.get_id)
        return resp
    else:
        print(active_user.is_authenticated,'this is get')
        print(current_user.get_id)
        print(request.headers.get('Authorization'))
        if current_user.is_authenticated:
            response=flask.make_response("user is online")
        else:
            response=flask.make_response("user is offline")
        return response
        

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    current_user.delete_key()
    logout_user()
    return jsonify(['user logout'])
        
             
