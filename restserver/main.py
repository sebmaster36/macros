#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Macros/Globals

QUERY_FIELDS    = {'crb', 'fat', 'prt', 'sgr'} # will/should be database entries in future
QUERY_OPS       = {'lt':'<', 'eq':'=', 'gt':'>'}
MAX_PARAMS      = len(QUERY_FIELDS)
MOD_NAME        = 'food_model'
DB_NAME         = 'database.db'

def db_query(wheres: list):
    '''
    takes in a list of clauses obtained from query string of request to /foods/query endpoint,
    opens a connection to database, executes query, and returns a list of tuples containing result 
    '''
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    clauses = ' and '.join(wheres) 
    query   = f'select * from {MOD_NAME} where ' + clauses # may not be the best practice 
    cur.execute(query)
    print(query)

    result = cur.fetchall()
    con.close()

    return result

# Models

# Defining ORM model for Food
class FoodModel(db.Model):
    fid = db.Column(db.Integer, primary_key=True)
    nme = db.Column(db.String(110), nullable=False)
    wgt = db.Column(db.Float, nullable=True)
    srv = db.Column(db.String(30), nullable=True) 
    prt = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    crb = db.Column(db.Float, nullable=True)
    sgr = db.Column(db.Float, nullable=True) # make default == 0?


# Necessary for output of db_query to be serializable by marshal with resource_fields envelope
class Food:
    def __init__(self, fid, nme, wgt, srv, prt, fat, crb, sgr):
        self.fid = fid 
        self.nme = nme
        self.wgt = wgt
        self.srv = srv
        self.prt = prt
        self.fat = fat
        self.crb = crb
        self.sgr = sgr

# db.create_all() # uncomment if redesigning ORM schema

# Landing Page

@app.route('/')
def landing():
    return '<h1>Welcome to the foods API!<h1>'

# API Endpoints & Setup 

# envelope for marshal tp serialize
resource_fields = { # serialization for marshal; DB model/class object -> JSON
    "id":       fields.Integer(attribute='fid'),
    "name":     fields.String(attribute='nme'),
    "weight":   fields.Float(attribute='wgt'),      
    "serving":  fields.String(attribute='srv'),
    "protein":  fields.Float(attribute='prt'),
    "fat":      fields.Float(attribute='fat'),
    "carbs":    fields.Float(attribute='crb'),
    "sugar":    fields.Float(attribute='sgr')
}


class FoodsList(Resource): # endpoint for all foods in DB
    def get(self):
        result = FoodModel.query.order_by(FoodModel.nme).all()
        return [ marshal(food, resource_fields) for food in result ]

class FoodsByID(Resource): # endpoint for specific food 
    def get(self, fid):
        result = FoodModel.query.filter_by(fid=fid)
        if not result or result is None:
            abort(404, message=f'no result matching id {fid} found.')

        return [ marshal(food, resource_fields) for food in result ]
        
class FoodsByQuery(Resource): # endpoint for foods meeting parameters
    def get(self):

        clause_list = [] 
        params      = request.args      


        # Error Handling
        if len(params) > MAX_PARAMS or len(params) == 0:
            abort(404, message="incorrect number of query parameters")
        ''' 
        iterating through ImmutableMultiDict (ex: ?fat=gt-4&fat=lt-3) eliminates potential 
        duplicates in query string, no need for check
        '''
        for item in params:
            if item not in QUERY_FIELDS:
                abort(404, message="invalid query parameter")

            try: 
                op, val = params[item].split('-') # normally prefer .get() but no need for defaults since iterating through existing keys
            except ValueError:
                abort(404, message="improperly formed query string") 
            
            if op not in QUERY_OPS:
                abort(404, message="invalid clause operation")

            # forming input to db_query; list item looks like 'food_model.fat > 5'
            clause_list.append(f'{MOD_NAME}.{item} {QUERY_OPS[op]} {val}')

        raw = db_query(clause_list)

        # output of db_query is list of tuples. transforming into serializable form
        result = [ Food(*raw_tuple) for raw_tuple in raw ]
        
        return [ marshal(food, resource_fields) for food in result ]

# configuring URLS
api.add_resource(FoodsList, '/api/v1.0/foods/')
api.add_resource(FoodsByID, '/api/v1.0/foods/<int:fid>')
api.add_resource(FoodsByQuery, '/api/v1.0/foods/query/')

# Guard
if __name__ == '__main__':
    app.run(debug=True)