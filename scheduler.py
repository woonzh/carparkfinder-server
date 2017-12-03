# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:28:55 2017

@author: ASUS
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import updateCarparkDets as ucd

sched = BlockingScheduler()

#@sched.scheduled_job('interval', days=7)
#def timed_job():
#    print('This job is run every week.')

@sched.scheduled_job('cron', day_of_week='mon', hour=1)
def scheduled_job():
    msg=ucd.main()
    print(msg+'\n'+'This job is run every monday at 1am.')

sched.start()