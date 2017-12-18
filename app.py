# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 15:00:01 2017

@author: ASUS
"""

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route("/carpark", methods=["POST"])
def post_to_db():
    return 'Success!'

if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True)