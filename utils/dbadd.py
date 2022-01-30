#!/usr/bin/env python3

'''
JSON parsing script for insertion into SQLite DB as FoodModel objects
'''

import json, sqlite3

DBPATH = '../restserver/database.db'
IDS = {'203', '204', '205', '269'}  # can easily add nutrients to start tracking (schema readjustment necessary)
FOODS = []

# type conversion that handles data anomalies
def conv(s: str):
    try:
        s_conv = float(s)
        return s_conv
    except ValueError:
        return None

class Food:
    def __init__(self, fid, nme, wgt, srv, pro, fat, crb, sgr):
        self.fid = fid
        self.nme = nme
        self.wgt = wgt
        self.srv = srv
        self.pro = pro
        self.fat = fat
        self.crb = crb
        self.sgr = sgr

    def __repr__(self):
        return f'{self.fid}'

def main():

    db = sqlite3.connect(DBPATH)
    cur = db.cursor()

    with open("food_data.json") as fd:
        raw = json.load(fd)

    # creating list of Food objects
    for food in raw['report']['foods']: # List(dict())
        
        cur.execute("INSERT INTO food_model VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                food['ndbno'], food['name'], food['weight'], food['measure'], 
                *(conv(nut['value']) for nut in food['nutrients'] if nut['nutrient_id'] in IDS)
            )
        )
    
    db.commit()
    db.close()
      
if __name__ == '__main__':
    main()