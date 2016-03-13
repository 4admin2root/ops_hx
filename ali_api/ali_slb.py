#!/usr/local/bin/python
# -*- coding:utf-8 -*- 
"""
阿里云slb api功能详细需求： 
1.根据slb名称模糊查询，slb相关信息（包括：可用区，服务地址，服务端口，后端服务器） 
2.根据后端服务器名称模糊查询，slb相关信息（包括：可用区，服务地址，服务端口，后端服务器） 
3.根据slb名称，进行操作：包括添加、减少后端服务器，调整服务器权重 
4.根据slb所在区域提供查询列表
"""
import sys
import csv
import json
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf8') 
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeRegionsRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
class HX_alislb:
 __version__ = '0.1'
 __all__ = ['listslbs_byname', 'listregions','addservers','rmservers','chweight' ]
 __author__ = 'lvzj'
 def __init__(self,slbname='',region='cn-qingdao',instancename='',LoadBalancerId='',ServerId=''):
      self.slbname = slbname
      self.region = region
      self.instancename = instancename
      self.accessKeyId = 'xc'
      self.accessKeySecret = 'we'
      self.LoadBalancerId = LoadBalancerId
      self.ServerId = ServerId
      self.clt = client.AcsClient(self.accessKeyId,self.accessKeySecret,self.region)
#
 def listregions(self):
     request = DescribeRegionsRequest.DescribeRegionsRequest()
     request.set_accept_format('json')
     result = self.clt.do_action(request)
     try :
           region_j = json.loads(result)
     except ValueError, e:
                print "json 格式错误"
                print e
                sys.exit(1)
     for i in region_j['Regions']['Region']:
	print i['LocalName']+'\t:'+i['RegionId']
#
 def __printslb(self,i,loadbalancername):
   slbinfo = i['RegionIdAlias']+'\t:'+loadbalancername+'\t:'+i['Address']+'\t:'+i['LoadBalancerStatus']+'\t:'
   request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
   request.set_accept_format('json')
   request.set_LoadBalancerId(i['LoadBalancerId'])
   result = self.clt.do_action(request)
   result_j = json.loads(result)
   slbinfo = slbinfo + str(result_j['ListenerPorts']['ListenerPort']) + '\t:'
   serverids = result_j['BackendServers']['BackendServer']
   for serverid in serverids:
       request = DescribeInstancesRequest.DescribeInstancesRequest()
       request.set_accept_format('json')
       request.set_InstanceIds('["'+serverid['ServerId']+'"]')
       result = self.clt.do_action(request)
       result_j = json.loads(result)
       slbinfo = slbinfo  + result_j['Instances']['Instance'][0]['InstanceName'] + ','
   print slbinfo
 def getinstaces_byname(self):
       request = DescribeInstancesRequest.DescribeInstancesRequest()
       request.set_accept_format('json')
       request.set_InstanceName(self.instancename)
       result = self.clt.do_action(request)
       result_j = json.loads(result)
       print result_j
 def getinstaces_bynamelike(self):
       request = DescribeInstancesRequest.DescribeInstancesRequest()
       request.set_accept_format('json')
       request.set_PageSize(100)
       result = self.clt.do_action(request)
       result_j = json.loads(result)
       for i in  result_j['Instances']['Instance']:
          if self.instancename in i['InstanceName']:
           print i['InstanceId']+ ':'+ i['InstanceName']
       if result_j['TotalCount']> 100:
          print result_j['TotalCount']
          pages = result_j['TotalCount']/100
          if result_j['TotalCount']%100 > 0 :
             pages = pages + 1
             
 def listslbs_bynamelike(self):
     request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
     request.set_accept_format('json')
     result = self.clt.do_action(request)
     try :
           region_j = json.loads(result)
     except ValueError, e:
                print "json 格式错误"
                print e
                sys.exit(1)
     for i in region_j['LoadBalancers']['LoadBalancer']:
        loadbalancername = ''
        try :
            loadbalancername = i['LoadBalancerName']
        except Exception, e:
            pass
        if self.slbname == '' :
           self.__printslb(i,loadbalancername)
        else :
           if self.slbname in loadbalancername :
              self.__printslb(i,loadbalancername)
 def listslb_byslbid(self):
     request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
     request.set_accept_format('json')
     request.set_set_LoadBalancerId(self.LoadBalancerId)
     result = self.clt.do_action(request)
     try :
           region_j = json.loads(result)
     except ValueError, e:
                print "json 格式错误"
                print e
                sys.exit(1)
     for i in region_j['LoadBalancers']['LoadBalancer']:
        loadbalancername = ''
        try :
            loadbalancername = i['LoadBalancerName']
        except Exception, e:
            pass
        if self.slbname == '' :
           self.__printslb(i,loadbalancername)
        else :
           if self.slbname in loadbalancername :
              self.__printslb(i,loadbalancername)
  
if __name__ == '__main__':
    regionlist = ['cn-beijing','cn-hangzhou','cn-qingdao','cn-hongkong']
    parser = OptionParser(usage='"usage:%prog [options] arg"',version="%prog 0.2")
    parser.add_option("-a","--action",dest="action",type="string",help="action:"+)
    parser.add_option("-s","--slb",dest="slbname",type="string",help="name of slb")
    parser.add_option("-x","--slbid",dest="slbid",type="string",help="id of slb")
    parser.add_option("-i","--instance",dest="instancename",type="string",help="name of instance")
    parser.add_option("-y","--insid",dest="instanceid",type="string",help="id of instance")
    parser.add_option("-r","--region",dest="region",type="string",help="name of region,as:"+"|".join(regionlist),default="cn-qingdao")
    if len(sys.argv) ==1 :
       parser.print_help()
       sys.exit(1)
    (options,args) = parser.parse_args()
    if len(args) != 0:
       parser.error(' number of args is not right')
       sys.exit(1)
    print "region is: "+options.region
    print "slbname keyword: "+options.slbname
    print "instancename keyword: "+options.instancename
    print "===================================="
    if options.region not in regionlist:
       print "maybe the region in not right, please make sure or get contact to lvzj"
       sys.exit(1)
    else :
       hx_alislb = HX_alislb(options.slbname,options.region,options.instancename)
       #hx_alislb.listregions()
       #hx_alislb.listslbs_bynamelike()
       #hx_alislb.getinstaces_byname()
       hx_alislb.getinstaces_bynamelike()
