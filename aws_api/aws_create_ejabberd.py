#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于如下两个文件
.aws/config
.aws/credentials
实现功能：输入创建 instance imageid and number
"""
import boto3
import types
import sys
import csv
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf8') 
class AwsCI:
 __version__ = '0.1'
 __all__ = ['checkimg', 'createins','printres', ]
 __author__ = 'lvzj'
 def __init__(self,imgid,instancetype,instancenum,start):
      self.imgid = imgid
      self.instancetype  = instancetype
      self.instancenum = instancenum 
      self.start = start 
      self.ec2 = boto3.resource('ec2')
      self.client = boto3.client('ec2')
      self.tag = 'pro4-aws-ca-ejabberd'
#get image id from my ami
 def checkimg(self):
     try : 
       response = self.client.describe_images(
       ImageIds=[
        self.imgid,
          ]
       )
     except Exception,e:
      print e
      print "get imageid failed"
      sys.exit(1)
 def createins(self):
   try :
    self.instances = self.ec2.create_instances(
    ImageId=self.imgid,
    MinCount=self.instancenum,                             #please change
    MaxCount=self.instancenum,                             #please change
    KeyName='easemob',
    InstanceType=self.instancetype,                      ## please change 
    Monitoring={
        'Enabled': False
    },
    DisableApiTermination= True,
    InstanceInitiatedShutdownBehavior='stop',
    NetworkInterfaces=[
        {
            'DeviceIndex': 0,
            'SubnetId': 'subnet-330ad756',
            'Groups': [
                'sg-a8df07cd',
               ],
            'DeleteOnTermination': True,
            'AssociatePublicIpAddress': False
        },
    ],
    EbsOptimized=True, # for test,in product please set true
    )
   except Exception,e:
       print e
       print "create instances error,please check the parameters and error msg above" 
       sys.exit(1)
   try:
    tagid=self.start
    for instance in self.instances:
        tag = instance.create_tags(Tags=[{'Key':'Name','Value':self.tag+str(tagid)},{'Key':'Desc','Value':'created by aws_create_ejabberd.py'}])
        tagid += 1
   except Exception,e:
       print e
       print "create tag failed, please login aws console to check"
       sys.exit()
 def printres(self):
     l_hosts=[]
     try:
      for instance in self.instances:
         if instance.tags[0]['Key'] == 'Name' :
             name = instance.tags[0]['Value']
         else :
             name = instance.tags[1]['Value']
         print instance.instance_id + "__" + instance.private_ip_address + " " + name
         l_hosts.append(instance.private_ip_address + " " + name+"\n")
     except Exception,e:
         print e
         print "print result error"
         sys.exit(1)
     try :
         fp=open("hosts",'w')
         fp.writelines(l_hosts)
         fp.close()
     except Exception ,e:
         print e
         sys.exit(1)
if __name__ == '__main__':
    print "注意此脚本将导致服务器数量变动,具体情况还需手动到aws console上确认"
    typelist = ['t2.micro','r3.2xlarge','i2.8xlarge','m2.4xlarge','r3.4xlarge','m2.xlarge','r3.large','r3.8xlarge','c1.xlarge','i2.xlarge','g2.2xlarge','m2.2xlarge','m1.medium','g2.8xlarge','c4.xlarge','c4.large','c4.4xlarge','c4.2xlarge','c3.large','c4.8xlarge','c3.2xlarge','c3.xlarge','c3.8xlarge','c3.4xlarge','m1.small','r3.xlarge','i2.2xlarge','i2.4xlarge','c1.medium','m1.xlarge','m4.large','m1.large','m4.2xlarge','m4.xlarge','m4.10xlarge','m4.4xlarge','m3.large','m3.medium','m3.2xlarge','m3.xlarge']
    parser = OptionParser(
        usage="""usage:%prog [options] arg
      for example:  python aws_create_ejabberd.py -s 40 -t m4.4xlarge -m ami-470d7327 -n 2
               """, version="%prog 0.2")
    parser.add_option(
        "-s", "--start", dest="istart", type="int", help="start from of instance name suffix")
    parser.add_option(
        "-t", "--type", dest="itype", type="string", help="type of instance")
    parser.add_option(
        "-m", "--ami", dest="iami", type="string", help="ami of instance")
    parser.add_option(
        "-n", "--num", dest="inum", type="int", help="number of instances")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error(' number of args is not right')
        sys.exit(1)
    if options.inum > 20 :
       print "instance number can't be more than 20"
       sys.exit(1)
    print "image id is: "+options.iami
    print "instance type is: "+options.itype
    if options.itype not in typelist:
       print "maybe the instance type in not right, please make sure or get contact to lvzj"
       sys.exit(1)
    if type(options.inum) == types.NoneType:
              options.inum = 1
    awsci= AwsCI(options.iami,options.itype,options.inum,options.istart)
    awsci.checkimg()
    awsci.createins()
    print "========="
    awsci.printres()
