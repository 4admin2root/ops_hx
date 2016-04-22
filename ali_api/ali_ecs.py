#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
please change the accessKeyId accessKeySecret and Password
search 'xxx'
"""
import types
import sys
import time
import csv
import json
import csv
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf8')
from aliyunsdkcore  import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import DescribeZonesRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest


class HX_aliecs:
    __version__ = '0.1'
    __author__ = 'lvzj'

    def __init__(self, region='cn-qingdao'):
        self.region = region
        self.accessKeyId = 'Btw5QMNJq8qrdD8Q'
        self.accessKeySecret = 'aJY6VZ55rAFURMly8HY903TidC0fav'
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
    def listzones(self):
        request = DescribeZonesRequest.DescribeZonesRequest()
        request.set_accept_format('json')
        result = self.clt.do_action(request)
        try:
            zone_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in zone_j['Zones']['Zone']:
            print "ZoneId:"+i['ZoneId']

    def listinstancetypes(self):
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        request.set_accept_format('json')
        result = self.clt.do_action(request)
        try:
            type_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in type_j['InstanceTypes']['InstanceType']:
            print 'InstanceType:'+i['InstanceTypeId']+'|' + 'cpu:'+str(i['CpuCoreCount'])+'|'+'memory:'+str(i['MemorySize'])

    def listsecuritygroups(self):
        request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
        request.set_accept_format('json')
        result = self.clt.do_action(request)
        try:
            sec_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in sec_j['SecurityGroups']['SecurityGroup']:
            print 'SecurityGroupId:'+i['SecurityGroupId']+'|'+'SecurityGroupName:'+i['SecurityGroupName']
 
    def listimages(self):
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)
        request.set_ImageOwnerAlias('self')
        result = self.clt.do_action(request)
        try:
            image_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        for i in image_j['Images']['Image']:
            print 'ImageId:'+i['ImageId']+'|'+'ImageName:'+i['ImageName']

    def createinstance(self,iname,itype,iimg,isg,izone,ids,id1s,ibw,idssd,id1ssd,chargetype,withpubip):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceType(itype)
        request.set_SecurityGroupId(isg)
        request.set_ImageId(iimg)
        request.set_InstanceName(iname)
        request.set_Description('xxx')
        request.set_InternetChargeType('xxx')
        request.set_InternetMaxBandwidthOut(ibw)
        request.set_ZoneId(izone)
        request.set_Password('xxx')
        request.set_SystemDiskSize(ids)
        if idssd == True:
            request.set_SystemDiskCategory('cloud_ssd')
        if id1ssd == True:
            request.set_DataDisk1Category('cloud_ssd')
        #request.set_SystemDiskCategory('cloud_ssd')
        if id1s <> 0:
            request.set_DataDisk1Size(id1s)
        #request.set_DataDisk1Category('cloud_ssd')
        if chargetype == True:
            request.set_InstanceChargeType('PrePaid')
            request.set_Period(1)
        result = self.clt.do_action(request)
        try:
            instance_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
        try:
            print "the new instanceid is: "+instance_j['InstanceId']
        except Exception,e:
            print "create instance failed!!"   
            print instance_j  
            sys.exit(1)
       #sleep to wait for alisdk and then print instance info
        time.sleep(5)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_InstanceIds([str(instance_j['InstanceId'])])
        result = self.clt.do_action(request)
        iresult_j = json.loads(result)
        for i in iresult_j['Instances']['Instance']:
            print 'PrivateIpAddress:' + i['InnerIpAddress']['IpAddress'][0]
            print 'Cpu:' + str(i['Cpu'])
            print 'Memory:' + str(i['Memory'])
        #assign public ip address and print it
        if withpubip == True and instance_j['InstanceId']:
            request=AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
            request.set_accept_format('json')
            request.set_InstanceId(instance_j['InstanceId'])
            result = self.clt.do_action(request)
            pub_j = json.loads(result)
            print "PublicIpAddress:"+pub_j['IpAddress']
       #start instance
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(instance_j['InstanceId'])
        request.set_accept_format('json')
        result = self.clt.do_action(request)
        try:
            ires_j = json.loads(result)
        except ValueError, e:
            print "json 格式错误"
            print e
            sys.exit(1)
    def getinstanceinfo_byid(self, instanceid):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_InstanceIds([instanceid])
        result = self.clt.do_action(request)
        result_j = json.loads(result)
        for i in result_j['Instances']['Instance']:
            print "============================="
            print 'InstanceId:' + i['InstanceId']
            print 'InstanceName:' + i['InstanceName']
            print 'CreationTime:' + i['CreationTime']
            print 'ExpiredTime:' + i['ExpiredTime']
            print 'Status:' + i['Status']
            print 'IpAddress:' + i['InnerIpAddress']['IpAddress'][0]
            publicip = ''
            try :
                publicip = i['PublicIpAddress']['IpAddress'][0]
            except Exception,e:
                pass
            print 'PublicIpAddress:' + publicip
            print 'Cpu:' + str(i['Cpu'])
            print 'Memory:' + str(i['Memory'])


if __name__ == '__main__':
    regionlist = ['cn-beijing', 'cn-hangzhou', 'cn-qingdao', 'cn-hongkong','cn-shanghai','cn-shenzhen','us-east-1','us-west-1','ap-southeast-1']
    parser = OptionParser(
        usage="""usage:%prog [options] arg
      for example:  python ali_ecs.py -n sdb_docker_test -t ecs.s3.large -m m-23g1lkoue -s G1096298575498592 -z cn-hangzhou-d -d 40 -r cn-hangzhou -p
               """, version="%prog 0.2")
    parser.add_option(
        "-n", "--name", dest="iname", type="string", help="name of instance")
    parser.add_option(
        "-t", "--type", dest="itype", type="string", help="type of instance")
    parser.add_option(
        "-d", "--ids", dest="ids", type="int", help="size(G) of instance system disk")
    parser.add_option(
        "-e", "--id1s", dest="id1s", type="int", help="size(G) of instance data disk")
    parser.add_option(
        "-w", "--ibw", dest="ibw", type="int", help="Bandwidth of instance")
    parser.add_option(
        "-y", "--id1ssd", action="store_true",dest="id1ssd",  help=" set the Category of data disk to ssd")
    parser.add_option(
        "-x", "--idssd", action="store_true",dest="idssd",  help=" set the Category of system disk to ssd")
    parser.add_option(
        "-m", "--img", dest="iimg", type="string", help="image id of instance")
    parser.add_option(
        "-z", "--izone", dest="izone", type="string", help="zone id of instance")
    parser.add_option(
        "-s", "--isg", dest="isg", type="string", help="security group id of instance")
    parser.add_option(
        "-l", "--listinfo", action="store_true",dest="listinfo",  help="listinfo:region,image,type")
    parser.add_option(
        "-c", "--chargetype", action="store_true",dest="chargetype",  help="is prepaid ?")
    parser.add_option(
        "-p", "--withpubip", action="store_true",dest="withpubip",  help="with public ip ?")
    parser.add_option(
        "-r", "--region", dest="region", type="string",
        help="name of region,as:" + "|".join(regionlist), default="cn-qingdao"
         )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error(' number of args is not right')
        sys.exit(1)
    print "region is: " + options.region
    if options.region not in regionlist:
        print "maybe the region is not right, please make sure or get contact to lvzj"
        sys.exit(1)
    print "===================================="
    # if options.instancename and options.instanceid:
    #    parser.error('you can not specify instancenπame and instanceid at the same time')
    #    sys.exit(1)
    hx_aliecs = HX_aliecs(options.region)
    if options.listinfo :
           print "#########"
           hx_aliecs.listregions()
           print "#########"
           hx_aliecs.listinstancetypes()
           print "#########"
           hx_aliecs.listimages()
           print "#########"
           hx_aliecs.listsecuritygroups()
           print "#########"
           hx_aliecs.listzones()
           print "#########"
    else :
           #hx_aliecs.createinstance(options.itype,options.isg,options.iimg,options.iname,options.izone,options.ids,options.id1s)
           #hx_aliecs.createinstance()
           #hx_aliecs.startinstance()
           if types.NoneType in [type(options.iname),type(options.itype),type(options.ids),type(options.iimg),type(options.isg),type(options.izone)]:
		parser.print_help()
		sys.exit(1)
           print "instance name is: " + options.iname
           print "instance type is: " + options.itype
           print "system disk size is: " + str(options.ids)
           if type(options.id1s) == types.NoneType:
              options.id1s = 0
           if type(options.ibw) == types.NoneType:
              options.ibw = 0
           if type(options.idssd) == types.NoneType:
              options.idssd = False 
           if type(options.id1ssd) == types.NoneType:
              options.id1ssd = False
           if type(options.chargetype) == types.NoneType:
              options.chargetype = False
           if type(options.withpubip) == types.NoneType:
              options.withpubip = False
           print "data disk size is: " + str(options.id1s)
           print "image id is: " + options.iimg
           print "securitygroup id is: " + options.isg
           print "zone is: " + str(options.izone)
           print "===================================="
           hx_aliecs.createinstance(options.iname,options.itype,options.iimg,options.isg,options.izone,options.ids,options.id1s,options.ibw,options.idssd,options.id1ssd,options.chargetype,options.withpubip)
           #hx_aliecs.getinstanceinfo_byid('i-23injsy2i')
