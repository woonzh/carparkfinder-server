# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 15:00:01 2017

@author: ASUS
"""

from flask import Flask, request
from flask_restful import Resource, Api
import carparkfuncs as of
import json

app = Flask(__name__)
api = Api(app)

class Carpark(Resource):
    def post(self):
        url="postgres://tmlzqhgujcsokr:2eded1d0ad12f58a6ff45a35fb68bc323465f8b3b1b28f147660d6a7bd3216b1@ec2-54-221-244-196.compute-1.amazonaws.com:5432/d43e472aa1ptv7"
        query="""SELECT * FROM cp_info"""
        cur, conn = of.connectToDatabase(url)
        
        cur.execute(query)
        msg=cur.fetchall()
        
        colnames = [desc[0] for desc in cur.description]
        df=[]

        for ent in msg:
            tstr={}
            for i in range(len(ent)):
                tstr[colnames[i]]=ent[i]
            
            df.append(tstr)
#            df += 'carpark:'+ str(tstr) +','

        df2={}
        df2["carparks"]=str(df)
        
        cur.close()
        
        return json.dumps(df2)

#t= Carpark
#msg=t.post('')

#d={'test':'tt'}
#df=json.loads(msg)
    
api.add_resource(Carpark, '/carpark') # Route_1

if __name__ == '__main__':
     app.run(debug=True)