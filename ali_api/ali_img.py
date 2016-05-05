#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
please change the accessKeyId accessKeySecret and Password
"""
import types
import ConfigParser
import os
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
from aliyunsdkecs.request.v20140526 import DescribeDisksRequest
from aliyunsdkecs.request.v20140526 import CreateSnapshotRequest
from aliyunsdkecs.request.v20140526 import CreateImageRequest


class HX_aliecs:
    __version__ = '0.1'
    __author__ = 'lvzj'

    def __init__(self, region='cn-qingdao'):
        self.region = region
        self.systemdiskid=''
        self.datadiskids=[]
        self.systemsnapid=''
        self.datasnapids=[]
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
    def getdiskinfo_byinstanceid(self, instanceid):
        request = DescribeDisksRequest.DescribeDisksRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instanceid)
        try :
            result = self.clt.do_action(request)
            diskinfo = json.loads(result)
        except Exception,e:
            print e
            sys.exit(1)
        for i in diskinfo['Disks']['Disk']:
            if i['Type'] == 'system':
                self.systemdiskid=i['DiskId']
            if i['Type'] == 'data':
                self.datadiskids.append(i['DiskId'])
    def create_image(self):
        request = CreateImageRequest.CreateImageRequest()
        request.set_accept_format('json')
        request.set_SnapshotId(self.systemsnapid)
        request.set_ImageName('with_'+'_'.join(self.datasnapids))
        try :
            result = self.clt.do_action(request)
            imginfo = json.loads(result)
        except Exception,e:
            print e
        print imginfo
        print imginfo['ImageId'] 
    def create_snapshot(self):
        request = CreateSnapshotRequest.CreateSnapshotRequest()
        request.set_accept_format('json')
        request.set_DiskId(self.systemdiskid)
        request.set_SnapshotName('created_by_ali_img_py')
        try :
            result = self.clt.do_action(request)
            snapinfo = json.loads(result)
        except Exception,e:
            print e
            sys.exit(1)
        self.systemsnapid=snapinfo['SnapshotId']
        print 'system snapshot id:'+ self.systemsnapid
        for did in self.datadiskids:
           request = CreateSnapshotRequest.CreateSnapshotRequest()
           request.set_accept_format('json')
           request.set_DiskId(did)
           request.set_SnapshotName('created_by_ali_img_py')
           result = self.clt.do_action(request)
           snapinfo = json.loads(result)
           self.datasnapids.append(snapinfo['SnapshotId'])
        print 'data snapshot ids:'+ ','.join(self.datasnapids)
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


if __name__ == '__main__':
    regionlist = ['cn-beijing', 'cn-hangzhou', 'cn-qingdao', 'cn-hongkong','cn-shanghai','cn-shenzhen','us-east-1','us-west-1','ap-southeast-1']
    parser = OptionParser(
        usage="""usage:%prog [options] arg
      for example:  python ali_ecs.py -i i-dfsdf -d  -r cn-hangzhou 
               """, version="%prog 0.2")
    parser.add_option(
        "-l", "--list", dest="listinfo", action="store_true", help="print image list")
    parser.add_option(
        "-i", "--instanceid", dest="instanceid", type="string", help="id of instance")
    parser.add_option(
        "-d", "--datadisk", action="store_true",dest="withdatadisk",  help="with data disk ?")
    parser.add_option(
        "-r", "--region", dest="region", type="string",
        help="name of region,as: " + "|".join(regionlist), default="cn-qingdao"
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
           hx_aliecs.listimages()
           print "#########"
    else :
           hx_aliecs.getdiskinfo_byinstanceid(options.instanceid)
           hx_aliecs.create_snapshot()
           #hx_aliecs.create_image(){u'Code': u'InvalidSnapshotId.NotReady', u'Message': u'The specified snapshot creation is not completed yet.', u'HostId': u'ecs-cn-hangzhou.aliyuncs.com', u'RequestId': u'F706A881-5F8A-4CF0-BBF3-9E013C5A3EE9'}
