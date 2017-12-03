# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:39:42 2017

@author: woon.zhenhao
"""

import pandas as pd
import carparkfuncs as of

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

cpavail=pd.DataFrame(columns=['car_park_no','lots avail', 'total lots', 'percen full'])

for res in range(len(cpava)):
    df=cpava[res]
    df2=df['carpark_info'][0]
    percen=(int(df2['lots_available'])/int(df2['total_lots']))*100
    cpavail.loc[res]=([df['carpark_number'],df2['lots_available'],df2['total_lots'],percen])


cp=cpavail.merge(cpinfo, on='car_park_no', how='left')
#
cpclean, summary=of.removeNullRows(cp)


#lat=[]
#lng=[]
#for ind in range(len(cpclean)):
#    add=cpclean.iloc[ind,4]
#    latv, lngv=of.coordRet(add)
#    lat.append(latv)
#    lng.append(lngv)
##    
#cpclean['lat']=lat
#cpclean['lng']=lng
##
#cpclean2, summary2= of.removeNullRows(cpclean)
#
#cpclean2.to_csv('carpark avail.csv')