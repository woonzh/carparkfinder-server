# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:39:42 2017

@author: woon.zhenhao
"""

import pandas as pd
import carparkfuncs as of
import time

def main():
    start= time.time()
    
    cpinfo=of.jsonRetriever('https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c&limit=2000'
                            ,'api-key'
                            ,'lT4tVeyqPFXK4SChuNN0jzx6O11Dq6nF')
    cpinfo=pd.io.json.json_normalize((cpinfo['result'])['records'])
    cpinfo=pd.DataFrame(cpinfo['car_park_no'])
    
    cpavail=of.jsonRetriever('https://api.data.gov.sg/v1/transport/carpark-availability?date_time=2017-09-11T09:45:00'
                            ,'api-key'
                            ,'lT4tVeyqPFXK4SChuNN0jzx6O11Dq6nF')
    cpava=cpavail['items'][0]
    cpava=cpava['carpark_data']
    
    cpavail=pd.DataFrame(columns=['lots avail', 'total lots', 'percen full', 'car_park_no'])
    
    for res in range(len(cpava)):
        df=cpava[res]
        df2=df['carpark_info'][0]
        percen=(int(df2['lots_available'])/int(df2['total_lots']))*100
        cpavail.loc[res]=([df2['lots_available'],df2['total_lots'],percen,df['carpark_number']])
    
    
    cp=cpavail.merge(cpinfo, on='car_park_no', how='left')
    #
    cpclean, summary=of.removeNullRows(cp)
    
    t1=time.time()
    print('Process API time: '+str(t1-start)+' secs')
    
    t1=time.time()
    
    url="postgres://tmlzqhgujcsokr:2eded1d0ad12f58a6ff45a35fb68bc323465f8b3b1b28f147660d6a7bd3216b1@ec2-54-221-244-196.compute-1.amazonaws.com:5432/d43e472aa1ptv7"
        
    sql = """UPDATE cp_info
                 SET avail_lots=%s, tot_lots=%s, empty_percen=%s
                 WHERE car_park_no=%s;"""
    
    df=[tuple(x) for x in cpclean.values]
    
    msg=of.updateCapacity(url,sql,df,False)
    
    t2=time.time()
    print('Update database time: '+str(t2-t1)+' secs')
