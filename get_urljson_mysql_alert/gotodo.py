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
from Connalert import *

signal.signal(signal.SIGCHLD,signal.SIG_IGN)
while True :
   try :
      pid = os.fork()
      if pid == 0:
       try :
        c = Connalert('a.out','http://121.41.37.xx:8080/getallconnect','xx','xx','localhost',3306,'root','')
        c.getjson()
        c.domysql()
        c.doprint()
        os._exit(0)
        print 'children'
       except Exception,e:
        print e
   except OSError, e:
     print e
   print 'before sleep' 
   time.sleep(60) 
   print 'after sleep'
