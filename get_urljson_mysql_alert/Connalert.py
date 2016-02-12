#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
#读取文件，url，取到json
#打开mysql数据库连接，存入json
#读取mysql中表conn_threshold，配置告警项目和阈值
#处理异常
#如对方为公网地址则暂不处理
#多次告警，入库，并忽略
#mysql数据保留一天
#deamon
"""
import os
import time
import datetime
import urllib2
import MySQLdb
import json
import math
import sys
import signal
reload(sys) 
sys.setdefaultencoding('utf8')
class Connalert:
 
 __version__ = '0.1'
 __all__ = [
    'getjson', 'domysql','doprint',
  ]

 __author__ = 'lvzj'

 def __init__(self,outfile,url,username,password,sqlhost,sqlport,sqlu,sqlp):
   self.Outfile = outfile
   self.Username = username
   self.Password = password
   self.Url = url
   self.Sqlhost = sqlhost
   self.Sqlport = sqlport
   self.Sqlu = sqlu
   self.Sqlp = sqlp
   try :
      Of = open(self.Outfile,'a')
   except Exception,e:
      print "打开文件失败"
      sys.exit()
   sys.stdout = Of 
   self.json = ''
   self.emsg = []

 def getjson(self):
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None,self.Url,self.Username,self.Password)
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)
	try:
		response = urllib2.urlopen(self.Url,timeout=5) 
		jsonstr = response.read() 
	except urllib2.HTTPError,e:
		print e.code
		print e.read()
        try :
           self.json = json.loads(jsonstr)
        except ValueError, e:
                print "json 格式错误" 
                sys.exit()
 def domysql(self):
  dtnow = datetime.datetime.now()
  dt = dtnow.strftime('%Y-%m-%d %H:%M:%S')
  try:
    conn=MySQLdb.connect(host=self.Sqlhost,port=self.Sqlport,user=self.Sqlu,passwd=self.Sqlp,db='conncount',charset="utf8")
  except Exception,e:
    print e
    print "连接数据库失败"
    sys.exit()
  try:
    conn.autocommit(1)
    cur=conn.cursor()
    #获取上次所有连接名信息
    dt1 = dtnow + datetime.timedelta(minutes=-1)
    getallsql = "select distinct connects from getlog where logdt like '"+dt1.strftime('%Y-%m-%d %H:%M')+"%'" 
    cur.execute(getallsql)
    lastall = cur.fetchall()
    if len(lastall) == 0 :
        msg = "warn: the number of last getlog is 0"
        esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
        self.emsg.append(msg)
        cur.execute(esql)
    #获取阈值信息
    thresholdsql = "select connects,num  from conn_threshold" 
    cur.execute(thresholdsql)
    thresholdinfo = cur.fetchall()
    zthresholdinfo = zip(*thresholdinfo) 
    nowall = []
    #插入本次获取连接信息
    for i in self.json :
        isql = """insert into getlog values('""" + i['connect'] + "'," + str(i['count']) + "," + str(i['change']) + ",'" + str(dt) + "')"
        cur.execute(isql)
        nowall.append(i['connect'])
	if i['change'] != 0:
          if len(thresholdinfo) > 0:
                if i['connect'] in zthresholdinfo[0]:
                    p = zthresholdinfo[0].index(i['connect'])
                    if math.fabs(i['change']) > zthresholdinfo[1][p] :
                       msg = "超阈值连接数告警:"+i['connect']+" 当前值:"+str(i['count'])+" 变化值:"+str(i['change'])
                       self.emsg.append(msg)
                       esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
                       cur.execute(esql)
                else : 
                   msg = "连接数告警:"+i['connect']+" 当前值:"+str(i['count'])+" 变化值:"+str(i['change'])
                   self.emsg.append(msg)
                   esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
                   cur.execute(esql)
          else :
                   msg = "连接数告警:"+i['connect']+" 当前值:"+str(i['count'])+" 变化值:"+str(i['change'])
                   self.emsg.append(msg)
                   esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
                   cur.execute(esql)

#       long not <  and != long
    #查找出不存在的连接
    if len(lastall) > 0 :
     for i in lastall :
        if i[0] not in nowall :
         msg = "存在消失的连接:" + i[0]
         esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
         self.emsg.append(msg)
         cur.execute(esql)
    cur.close()
    conn.commit()
    conn.close()
  except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
     sys.exit()


 def doprint(self) :
  if len(self.emsg) < 10 :
   for i in  self.emsg:
       print "emsg:" + i
  else : 
   print "哥几个,连接告警数超过10个了,处理下吧"
   for i in range(0,4):
       print self.emsg[i]

if __name__ == '__main__':
        pidf = os.getpid()
        try :
            fpid = open('/tmp/Connalert.pid','w')
            fpid.write(str(pidf))
            fpid.close()
        except Exception,e:
         print e
         print "打开文件失败"
         sys.exit() 
        c = Connalert('a.out','http://121.41.37.xx:8080/getallconnect','xx','xx','localhost',3306,'root','')
        c.getjson()
        c.domysql()
        c.doprint()
        os.remove('/tmp/Connalert.pid')
