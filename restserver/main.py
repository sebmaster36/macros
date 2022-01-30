#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB models

class FoodModel(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    nme = db.Column(db.String(110), nullable=False)
    wgt = db.Column(db.Float, nullable=True)
    srv = db.Column(db.String(30), nullable=True) 
    prt = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    crb = db.Column(db.Float, nullable=True)
    sgr = db.Column(db.Float, nullable=True)

    '''
    def __repr__(self):
        return f'dbno: {self.fid}'
    '''

# db.create_all() # uncomment if redesigning ORM schema

# Landing Page

@app.route('/')
def landing():
    return '<h1>Welcome to the foods API!<h1>'

# API Endpoints & Setup 

resource_fields = { # figure out how to restructure
    "id":       fields.Integer(attribute='fid'),
    "name":     fields.String(attribute='nme'),
    "weight":   fields.Float(attribute='wgt'),      
    "serving":  fields.String(attribute='srv'),
    "protein":  fields.Float(attribute='prt'),
    "fat":      fields.Float(attribute='fat'),
    "carbs":    fields.Float(attribute='crb'),
    "sugar":    fields.Float(attribute='sgr')
}

class FoodsListAPI(Resource):
    def get(self, crb, fat, pro, sug):
        print(crb, pro, fat, sug)


        result = FoodModel.query.order_by(FoodModel.nme).all()
        return [ marshal(food, resource_fields) for food in result ]
        
api.add_resource(FoodsListAPI, '/api/v1.0/foods/<float:crb>/<float:fat>/<float:pro>/<float:sug>', endpoint='foods')

if __name__ == '__main__':
    app.run(debug=True)

# could assert count(*) == len(foods) as a check