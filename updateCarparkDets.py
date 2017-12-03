# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 12:01:27 2017

@author: ASUS
"""

import pandas as pd
import carparkfuncs as of

def main():
    cpinfo=of.jsonRetriever('https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c&limit=2000'
                            ,'api-key'
                            ,'lT4tVeyqPFXK4SChuNN0jzx6O11Dq6nF')
    cpinfo=pd.io.json.json_normalize((cpinfo['result'])['records'])
    cpinfo.drop('_id', axis=1,inplace=True)
    
    cpavail=of.jsonRetriever('https://api.data.gov.sg/v1/transport/carpark-availability?date_time=2017-09-11T09:45:00'
                            ,'api-key'
                            ,'lT4tVeyqPFXK4SChuNN0jzx6O11Dq6nF')
    cpava=cpavail['items'][0]
    cpava=cpava['carpark_data']
    
    cpinfo2=pd.DataFrame(pd.io.json.json_normalize(cpava)['carpark_number'])
    cpinfo2.columns=['car_park_no']
    
    cp=cpinfo2.merge(cpinfo, on='car_park_no', how='left')
    cp=cp.drop_duplicates()
    
    cpclean, summary=of.removeNullRows(cp)
    
    lat=[]
    lng=[]
    for ind in range(len(cpclean)):
        add=cpclean.iloc[ind,1]
        latv, lngv=of.coordRet(add)
        lat.append(latv)
        lng.append(lngv)
        
    cpclean['lat']=lat
    cpclean['lng']=lng
    
    cpclean2, summary2= of.removeNullRows(cpclean)
    cpclean2.reset_index()
    
    cpclean2.drop(['type_of_parking_system', 'x_coord', 'y_coord'], axis=1,inplace=True)
    
    df=[tuple(x) for x in cpclean2.values]
    
    url="postgres://tmlzqhgujcsokr:2eded1d0ad12f58a6ff45a35fb68bc323465f8b3b1b28f147660d6a7bd3216b1@ec2-54-221-244-196.compute-1.amazonaws.com:5432/d43e472aa1ptv7"
    
    delsql = """DELETE FROM cp_info"""
    sql = """INSERT INTO cp_info
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    msg=of.updateDB(url,delsql, sql,df,False)
    
    return msg
