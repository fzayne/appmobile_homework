import json
from unittest import result
from app import app,db
from app.models import Item,User
from flask import render_template,jsonify, request


@app.route('/',methods=["POST", "GET"])
def index():
    global response
    u=User.query.get(1)
    if request.method=="POST":
        request_data=request.data
        request_data=json.loads(request_data.decode("utf-8"))
        data=request_data['data']
        i=Item(data=data,user=u)
        db.session.add(i)
        db.session.commit()
        return " "
    else:
       # cols=['id','type','data']
       #items=Item.query.get(2)
       #result=[{col: getattr(d,col) for col in cols} for d in items]
       #return jsonify(items)
        

        cols = ['id', 'type', 'data']
        data = Item.query.all()
        result = [{col: getattr(d, col) for col in cols} for d in data]
        return jsonify(result)
