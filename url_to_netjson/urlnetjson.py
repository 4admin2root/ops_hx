#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
"""
import os
import time
import datetime
import urllib2
import json
import sys
import re
class Node :
     def __init__(self) :
         self.id = ''
         self.label = 'nohostname'
class Link :
      def __init__(self) :
         self.source = ''
         self.target = ''
         self.cost = 1
class Netjson:
      def __init__(self) :
         self.type = 'Network'
         self.label = 'sdb-hangzhou'
         self.protocol = 'XXX'
         self.version = '0.0.0.1'
         self.metric = 'ETX'
         self.nodes = []
         self.links = []
      def setversion(self,ver) :
         self.version = ver
 
class Urlnetjson:
 __version__ = '0.1'
 __all__ = ['getjson', 'netjson', ]
 __author__ = 'lvzj'

 def __init__(self,url,username,password):
   self.Username = username
   self.Password = password
   self.Url = url
   self.json = ''
   self.netjson = Netjson()

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
                print e
                sys.exit()

 def getnetjson(self) :
     hosts = {}
     self.netjson.setversion(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
     try :
        f = open('hosts.txt','r')
        for line in f.readlines():
            lhosts = line.split()
            hosts[lhosts[0]]=lhosts[1]
     except Exception,e :
        print "读取hosts.txt文件失败"
     lnode = []
     for i in self.json :
         l = re.split('_|:',i['connect'])
         link = Link()
         link.source = l[2]
         link.target = l[0]
         self.netjson.links.append(link.__dict__)
         if l[0] not in lnode :
            lnode.append(l[0])
         if l[2] not in lnode :
            lnode.append(l[2])
     for i in lnode :
         node = Node()
         node.id = i
         if hosts.has_key(i) :
            node.label = hosts[i]
         else :
            node.label = i
         self.netjson.nodes.append(node.__dict__)
     print json.dumps(self.netjson.__dict__,ensure_ascii = False)
if __name__ == '__main__':
        pidf = os.getpid()
        try :
            fpid = open('/tmp/netjson.pid','w')
            fpid.write(str(pidf))
            fpid.close()
        except Exception,e:
         print e
         print "打开文件失败"
         sys.exit()
        c = Urlnetjson('http://121.41.37.xx:8080/getallconnect','xxx','xxxx')
        c.getjson()
        c.getnetjson()
        os.remove('/tmp/netjson.pid')
