#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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

    def __repr__(self):
        return f'dbno: {fid}'

# db.create_all() # uncomment if redesigning ORM schema

if __name__ == '__main__':
    app.run(debug=True)

# could assert count(*) == len(foods) as a check