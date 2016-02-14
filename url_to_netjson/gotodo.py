#!/usr/bin/python
# -*- coding:utf-8 -*-
"""

"""
import os
import time
import datetime
import sys
import signal
reload(sys)
sys.setdefaultencoding('utf8')
from urlnetjson import *
from apscheduler.schedulers.background import BackgroundScheduler

def gotodo():
        pidf = os.getpid()
        try :
            fpid = open('/tmp/netjson.pid','w')
            fpid.write(str(pidf))
            fpid.close()
        except Exception,e:
         print e
         sys.exit()
        c = Urlnetjson('http://xx:8080/getallconnect','xx','xx','/usr/share/nginx/html/test/data.json')
        c.getjson()
        c.getnetjson()
        c.savetofile()
        os.remove('/tmp/netjson.pid')
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(gotodo, 'interval', minutes=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown() 
