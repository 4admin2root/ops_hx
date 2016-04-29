#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
阿里云slb api功能详细需求：
1.根据slb名称模糊查询，slb相关信息（包括：可用区，服务地址，服务端口，后端服务器）
2.根据后端服务器名称模糊查询，slb相关信息（包括：可用区，服务地址，服务端口，后端服务器）
3.根据slb名称，进行操作：包括添加、减少后端服务器，调整服务器权重
4.根据slb所在区域提供查询列表
"""
import types
import ConfigParser
import os
import sys
import csv
import json
import csv
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf8')
from aliyunsdkcore  import client
from aliyunsdkslb.request.v20140515 import DescribeRegionsRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515 import AddBackendServersRequest
from aliyunsdkslb.request.v20140515 import RemoveBackendServersRequest
from aliyunsdkslb.request.v20140515 import SetBackendServersRequest


class HX_alislb:
    __version__ = '0.1'
    __all__ = ['listslbs_byname', 'listregions',
               'addservers', 'rmservers', 'chweight']
    __author__ = 'lvzj'

    def __init__(self, region='cn-qingdao'):
        self.region = region
        cf = ConfigParser.ConfigParser() 
        homepath = os.getenv("HOME")
        try :
            cf.read(homepath+"/.ali/credentials") 
            self.accessKeyId = cf.get("default","accessKeyId")
            self.accessKeySecret = cf.get("default","accessKeySecret")
        except Exception,e:
            print e
            sys.exit(1)
        self.clt = client.AcsClient(
            self.accessKeyId, self.accessKeySecret, self.region)
#

    def listregions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        result = self.clt.do_action(request)
        try:
            region_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in region_j['Regions']['Region']:
            print i['LocalName'] + '\t:' + i['RegionId']
# null is all

    def getslblist(self, slbid, instanceid):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        if len(slbid) != 0:
            request.set_LoadBalancerId(slbid)
        result = self.clt.do_action(request)
        try:
            region_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in region_j['LoadBalancers']['LoadBalancer']:
            lbname=''
            try :
                 lbname= i['LoadBalancerName']
            except Exception,e:
                 pass
            slbinfolist = [i['RegionIdAlias'], i['LoadBalancerId'],lbname, i['Address'], i['LoadBalancerStatus']]
            request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
            request.set_accept_format('json')
            request.set_LoadBalancerId(i['LoadBalancerId'])
            result = self.clt.do_action(request)
            result_j = json.loads(result)
            slbinfolist.append(str(result_j['ListenerPorts']['ListenerPort']))
            serverids = result_j['BackendServers']['BackendServer']
            serverinfolist = []
            if len(instanceid) == 0 or instanceid in serverids:
                for serverid in serverids:
                    request = DescribeInstancesRequest.DescribeInstancesRequest()
                    request.set_accept_format('json')
                    request.set_InstanceIds('["' + serverid['ServerId'] + '"]')
                    result = self.clt.do_action(request)
                    result_j = json.loads(result)
                    serverinfolist.append(
                        result_j['Instances']['Instance'][0]['InstanceName'])
            else:
                continue
            slbinfolist.append('|'.join(serverinfolist))
            print '\t'.join(slbinfolist)
            writer = csv.writer(
                file('ali_slb_info_' + self.region + '.csv', 'a'))
            writer.writerow(slbinfolist)

    def getinstanceinfo_byid(self, instanceid):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_InstanceIds([instanceid])
        result = self.clt.do_action(request)
        result_j = json.loads(result)
        for i in result_j['Instances']['Instance']:
            # print i
            print 'InstanceId:' + i['InstanceId']
            print 'InstanceName:' + i['InstanceName']
            print 'CreationTime:' + i['CreationTime']
            print 'ExpiredTime:' + i['ExpiredTime']
            print 'Status:' + i['Status']
            print 'IpAddress:' + i['InnerIpAddress']['IpAddress'][0]
            print 'PublicIpAddress:' + i['PublicIpAddress']['IpAddress'][0]
            print 'Cpu:' + str(i['Cpu'])
            print 'Memory:' + str(i['Memory'])

    def getinstances_bynamelike(self, instancename):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)
        result = self.clt.do_action(request)
        try:
            result_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)

        for i in result_j['Instances']['Instance']:
            if instancename in i['InstanceName']:
                print i['InstanceId'] + ':' + i['InstanceName']
        if result_j['TotalCount'] > 100:
            pages = result_j['TotalCount'] / 100
            if result_j['TotalCount'] % 100 > 0:
                pages = pages + 1
            pagecur = 2
            while pagecur <= pages:
                request = DescribeInstancesRequest.DescribeInstancesRequest()
                request.set_accept_format('json')
                request.set_PageSize(100)
                request.set_PageNumber(pagecur)
                result = self.clt.do_action(request)
                result_j = json.loads(result)
                for i in result_j['Instances']['Instance']:
                    if instancename in i['InstanceName']:
                        print i['InstanceId'] + ':' + i['InstanceName']
                pagecur += 1

    def getslbs_bynamelike(self, slbname):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        # request.set_PageSize(100)
        result = self.clt.do_action(request)
        try:
            result_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in result_j['LoadBalancers']['LoadBalancer']:
            lbname = ''
            try:
                lbname = i['LoadBalancerName']
            except Exception, e:
                lbname = ''
            if slbname in lbname:
                print i['LoadBalancerId'] + ':' + lbname

    def getslbinfo_byid(self, slbid):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slbid)
        result = self.clt.do_action(request)
        try:
            region_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in region_j['LoadBalancers']['LoadBalancer']:
            print 'LoadBalancerId:' + i['LoadBalancerId']
            print 'LoadBalancerName:' + i['LoadBalancerName']
            print 'CreateTime:' + i['CreateTime']
            print 'LoadBalancerStatus:' + i['LoadBalancerStatus']
            print 'Address:' + i['Address']

    def addbackendserver(self, slbid, instanceid,weight=100):
        request = AddBackendServersRequest.AddBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slbid)
        request.set_BackendServers("[{'ServerId':'"+instanceid+"','Weight':"+str(weight)+"}]")
        try: 
            result = self.clt.do_action(request)
        except Exception,e:
            print e

    def removebackendserver(self, slbid, instanceid):
        request = RemoveBackendServersRequest.RemoveBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slbid)
        request.set_BackendServers("[\""+instanceid+"\"]")
        try:
            result = self.clt.do_action(request)
        except Exception,e:
            print e
 
    def setbackendserver(self, slbid, instanceid, weight=100):
        request = SetBackendServersRequest.SetBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slbid)
        request.set_BackendServers("[{'ServerId':'"+instanceid+"','Weight':"+str(weight)+"}]")
        try:
            result = self.clt.do_action(request)
        except Exception,e:
            print e

    def createloadbalancer(self, instanceid, weight):
        pass


if __name__ == '__main__':
    regionlist = ['cn-beijing', 'cn-hangzhou', 'cn-qingdao', 'cn-hongkong']
    actionlist = ['lsr', 'getname', 'getinfo',
                  'getslblist', 'addserver', 'rmserver', 'chserver']
    slbinput = {}
    instanceinput = {}
    parser = OptionParser(
        usage='"usage:%prog [options] arg"', version="%prog 0.2")
    parser.add_option(
        "-a", "--action", dest="action", type="string",
        help="action:lsr,getname,getinfo,getslblist,addserver,rmserver,chserver",
        default="getname"
        )
    parser.add_option(
        "-s", "--slb", dest="slbname", type="string", help="name of slb")
    parser.add_option(
        "-x", "--slbid", dest="slbid", type="string", help="id of slb")
    parser.add_option(
        "-i", "--instance", dest="instancename", type="string",
        help="name of instance"
        )
    parser.add_option(
        "-y", "--insid", dest="instanceid", type="string",
        help="id of instance"
        )
    parser.add_option(
        "-w", "--weight", dest="weight", type="int", help="weight of instance")
    parser.add_option(
        "-r", "--region", dest="region", type="string",
        help="name of region,as:" + "|".join(regionlist), default="cn-qingdao"
         )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error(' number of args is not r  ight')
        sys.exit(1)
    print "region is: " + options.region
    print "action is: " + options.action
    if type(options.slbname) == types.NoneType:
        print "slbname keyword: is None"
    elif len(options.slbname) == 0:
        print "slbname keyword: is null"
        slbinput['null'] = True
    else:
        slbinput['name'] = options.slbname
        print "slbname keyword: " + options.slbname
    if type(options.instancename) == types.NoneType:
        print "instancename keyword: is None"
    elif len(options.instancename) == 0:
        print "instancename keyword: is null"
    else:
        instanceinput['name'] = options.instancename
        print "instancename keyword: " + options.instancename
    print "===================================="
    # if options.instancename and options.instanceid:
    #    parser.error('you can not specify instancenπame and instanceid at the same time')
    #    sys.exit(1)
    if options.action not in actionlist:
        print "maybe the action is not right"
        sys.exit(1)
    if options.region not in regionlist:
        print "maybe the region is not right, please make sure or get contact to lvzj"
        sys.exit(1)
    else:
        hx_alislb = HX_alislb(options.region)
        if options.action == 'getname':
            # hx_alislb.listregions()
            if type(options.instancename) == types.StringType:
                hx_alislb.getinstances_bynamelike(options.instancename)
            if type(options.slbname) == types.StringType:
                hx_alislb.getslbs_bynamelike(options.slbname)
        elif options.action == 'getinfo':
            if type(options.instanceid) == types.StringType:
                print '#' + options.instanceid
                hx_alislb.getinstanceinfo_byid(options.instanceid)
            if type(options.slbid) == types.StringType:
                print '#' + options.slbid
                hx_alislb.getslbinfo_byid(options.slbid)
        elif options.action == 'lsr':
            hx_alislb.listregions()
        elif options.action == 'getslblist':
            if type(options.slbid) == types.NoneType:
                options.slbid = ''
            if type(options.instanceid) == types.NoneType:
                options.instanceid = ''
            hx_alislb.getslblist(options.slbid, options.instanceid)
        elif options.action == 'addserver':
            if type(options.weight) == types.NoneType:
                options.weight = 100
            if type(options.slbid) == types.NoneType or type(options.instanceid) == types.NoneType :
                print "please provide specific both of slbid and instanceid"
                sys.exit(1)
            hx_alislb.addbackendserver(options.slbid,options.instanceid,options.weight)
        elif options.action == 'rmserver':
            if type(options.slbid) == types.NoneType or type(options.instanceid) == types.NoneType :
                print "please provide specific both of slbid and instanceid"
                sys.exit(1)
            hx_alislb.removebackendserver(options.slbid,options.instanceid)
        elif options.action == 'chserver':
            if type(options.slbid) == types.NoneType or type(options.instanceid) == types.NoneType :
                print "please provide specific both of slbid and instanceid"
                sys.exit(1)
            hx_alislb.setbackendserver(options.slbid,options.instanceid,options.weight)
