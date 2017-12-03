# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 09:54:28 2017

@author: woon.zhenhao
"""
import pandas as pd
import numpy as np
import json
import requests
import os
from urllib import parse
import psycopg2 as ps

def nullSummary(x):
    data = pd.DataFrame(x)
    listing = data.apply(lambda y: sum(y.isnull()),axis=0)
    return listing

def removeNullRows(x):
    #summary = nullSummary(x)
    colNames = list(x)
    k=x
    tot = 0
    tracker = pd.DataFrame(columns=['Removed Lines'])
    for col in colNames:
         rowId = k[k[col].isnull()].index
         tracker.loc[col]=len(rowId)
         tot = tot+len(rowId)
         k=k.drop(rowId)
         
    tracker.loc['Total']=tot
    tracker.loc['% Lost']=tot/len(x.index)
    
    k.index = np.arange(1,len(k)+1)
    
    return k, tracker

def removeSpaceRows(x):
    #summary = nullSummary(x)
    colNames = list(x)
    k=x
    tot = 0
    tracker = pd.DataFrame(columns=['Removed Lines'])
    for col in colNames:
         rowId = k[k[col].isspace()].index
         tracker.loc[col]=len(rowId)
         tot = tot+len(rowId)
         k=k.drop(rowId)
         
    tracker.loc['Total']=tot
    tracker.loc['% Lost']=tot/len(x.index)
    
    k.index = np.arange(1,len(k)+1)
    
    return k, tracker

def jsonRetriever(uri, header, headerVal):
    headers = { header : headerVal,'accept' : 'application/json'}

    url = uri
    
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return 'Null'

def coordRet(address):
    uri='https://maps.googleapis.com/maps/api/geocode/json?address='
    addclean = address.replace(' ','+') + ',+Singapore'
    apikey='AIzaSyAyN-6BT58IvVN4EMOGfMpUGuHbobeATfQ'
    url=uri+addclean+'&key='+apikey
        
    response = requests.get(url)
    lat=None
    lng=None
        
    if response.status_code == 200:
        df=json.loads(response.content.decode('utf-8'))

        if df['status']=='OK':
            df2=df['results']
            dc=pd.io.json.json_normalize(df2)
            lat=dc['geometry.location.lat'][0]
            lng=dc['geometry.location.lng'][0]
    
    return lat, lng

def processCPJson(x, dateStr):
    x=x['items'][0]
    x=x['carpark_data']
    
    avail=pd.DataFrame(columns=['carpark_number',dateStr])
    availPercen=pd.DataFrame(columns=['carpark_number',dateStr])

    for res in range(0,len(x)):
        t=x[res]
        t2=t['carpark_info'][0]
        avail.loc[res]=[str(t['carpark_number']),int(t2['lots_available'])]
        availPercen.loc[res]=[str(t['carpark_number']),int(t2['lots_available'])/int(t2['total_lots'])]
    
    return avail, availPercen

def saveFile(file, filename):
    file.to_csv(filename)
    
def connectToDatabase(url):
    os.environ['DATABASE_URL'] = url
               
    parse.uses_netloc.append('postgres')
    url=parse.urlparse(os.environ['DATABASE_URL'])
    
    conn=ps.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
            )
    
    cur=conn.cursor()
    
    return cur, conn
    
def updateDB(url, delQuery, query, data, retMsg):
    msg=[]
    try:
        cur, conn=connectToDatabase(url)
        
        cur.execute(delQuery)
        
        cur.executemany(query, data)
        if retMsg:
            msg.append(cur.fetchone())        
        
#        for i in data.index:
#            d=list(data.loc[i])
#            cur.execute(query, d)
#        
#            if retMsg:
#                msg.append(cur.fetchone())
        
        cur.close()
        conn.commit()
    
    except ps.Error as e:
        msg= e.pgerror
    
    return msg

    