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
import re
import MySQLdb
import json
import math
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
def getjsonstr(url,username,password):
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None,url,username,password)
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)
	try:
		response = urllib2.urlopen(url,timeout=5) 
		json = response.read() 
		return json 
	except urllib2.HTTPError,e:
		print e.code
		print e.read()
def domysql(js):
 dtnow = time.localtime(time.time())
 dt = time.strftime('%Y-%m-%d %H:%M:%S',dtnow)
 lastdtnow = datetime.datetime.now()
 emsg = []
 s = json.loads(js)
 try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='conncount',port=3306,charset="utf8")
    conn.autocommit(1)
    cur=conn.cursor()
    #获取上次所有连接
    dt1 = lastdtnow + datetime.timedelta(minutes=-1)
    getallsql = "select distinct connects from getlog where logdt like '"+dt1.strftime('%Y-%m-%d %H:%M')+"%'" 
    cur.execute(getallsql)
    lastall = cur.fetchall()
    nowall = []
    #插入本次获取连接信息
    for i in s :
        sql = """insert into getlog values('""" + i['connect'] + "'," + str(i['count']) + "," + str(i['change']) + ",'" + str(dt) + "')"
        cur.execute(sql)
        nowall.append(i['connect'])
	if i['change'] != 0:
		cur.execute("select max(num) from conn_threshold where connects = '" + i['connect']+"'")
		result = cur.fetchone()
		if type(result[0]) == long and result[0] < math.fabs(i['change']) :
                   #alert
                   msg = "连接数告警:"+i['connect']+" 当前值:"+str(i['count'])+" 变化值:"+str(i['change'])
		   emsg.append(msg)
		   esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
	           cur.execute(esql)
        cur.execute(sql)
    #查找出不存在的连接
    for i in lastall :
        if i not in nowall :
         msg = "存在消失的连接:"+i
         emsg.append(msg)
         esql = "insert into alertlog values('"+msg+"','"+str(dt)+"')"
         emsg.append(msg)
         cur.execute(esql)
    cur.close()
    conn.commit()
    conn.close()
    return emsg
 except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == '__main__':
 j = getjsonstr('http://xx:8080/getallconnect','xx','xx')
 emsg = domysql(j)
 if len(emsg) < 10 :
   for i in  emsg:
       print i
 else : 
   for i in range(0,4):
       print emsg[i]
       print "哥几个,连接告警数超过10个了,处理下吧"
