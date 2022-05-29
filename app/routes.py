import json
from flask_login import current_user, login_required,login_user, logout_user
from app import app,db
from app.models import Item,User
from flask import redirect, render_template,jsonify, request


@app.route('/',methods=["POST", "GET"])
def index():
    u=User.query.get(1)
    if request.method=="POST":
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        data=request_data['data']
        i=Item(data=data,user=u)
        db.session.add(i)
        db.session.commit()
        return "data saved successfully"
    else:
        cols = ['id', 'type', 'data']
        data = Item.query.all()
        result = [{col: getattr(d, col) for col in cols} for d in data]
        return jsonify(result)


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
                    return jsonify(['register success'])
                else:
                    return jsonify(['Please use a different email address.'])
            else:
                return jsonify(['Please use a different username.'])
        
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST": 
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        username=request_data['username']
        password=request_data['password']
        user =User.query.filter((User.username==username)|(User.email==username)).first()
        if user is None or not user.check_password(password):
            return jsonify(['wrong username or password']) 
        l=login_user(user,remember=True,force=True)
        if l==True:
            return jsonify(['login success'])
        else:
            return jsonify(["login failed"])
    else:
        if current_user.is_anonymous:
            return jsonify(['user is online'])
        else:
            return jsonify(['user is offline'])

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return jsonify(['user logout'])
        
             
