#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于如下两个文件
.aws/config
.aws/credentials
实现功能：输入创建instance的类型 数量 sdb磁盘空间GB 标签
"""
import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
class AwsCI:
 __version__ = '0.1'
 __all__ = ['checkimg', 'createins','printres', ]
 __author__ = 'lvzj'
 def __init__(self,instancetype,sdbsize,instancenum,tag):
      self.imgid = 'ami-8d668cc9'
      self.instancetype  = instancetype
      self.sdbsize = sdbsize
      self.instancenum = instancenum 
      self.ec2 = boto3.resource('ec2')
      self.client = boto3.client('ec2')
      self.tag = tag
      self.tagid = 0
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
    SecurityGroupIds=[
        'sg-a8df07cd'
    ],
    InstanceType=self.instancetype,                      ## please change 
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sdb',
            'Ebs': {
                'VolumeSize': self.sdbsize,                ## please change
                'DeleteOnTermination': True,
                'VolumeType': 'gp2',
                'Encrypted': False
                    },
        },
    ],
    Monitoring={
        'Enabled': False
    },
    SubnetId='subnet-330ad756',
    DisableApiTermination= False,
    InstanceInitiatedShutdownBehavior='stop',
    #EbsOptimized=True, # for test,in product please set true
    )
   except Exception,e:
       print e
       print "create instances error,please check the parameters and error msg above" 
       sys.exit(1)
   try:
    for instance in self.instances:
        self.tagid = self.tagid + 1
        tag = instance.create_tags(Tags=[{'Key':'Name','Value':self.tag+str(self.tagid)},])
   except Exception,e:
       print e
       print "create tag failed, please login aws console to check"
       sys.exit()
 def printres(self):
     try:
      for instance in self.instances:
         print instance.instance_id +"__"+ instance.public_ip_address +"__"+ instance.private_ip_address + " " + instance.tags[0]['Value']
     except Exception,e:
         print e
         print "print result error"
         sys.exit()
if __name__ == '__main__':
    print "注意此脚本将导致服务器数量变动,具体情况还需手动到aws console上确认"
    typelist = ['r3.2xlarge','i2.8xlarge','m2.4xlarge','r3.4xlarge','m2.xlarge','r3.large','r3.8xlarge','c1.xlarge','i2.xlarge','g2.2xlarge','m2.2xlarge','m1.medium','g2.8xlarge','c4.xlarge','c4.large','c4.4xlarge','c4.2xlarge','c3.large','c4.8xlarge','c3.2xlarge','c3.xlarge','c3.8xlarge','c3.4xlarge','m1.small','r3.xlarge','i2.2xlarge','i2.4xlarge','c1.medium','m1.xlarge','m4.large','m1.large','m4.2xlarge','m4.xlarge','m4.10xlarge','m4.4xlarge','m3.large','m3.medium','m3.2xlarge','m3.xlarge']
    if len(sys.argv) < 5:
          print "command format : python scritfilename --instancetype --sdbsize --instancenumber --tagname"
          print "\texample : python  aws_c_i.py --m3.large --30 --2 --pro4-aws-ca-test"
          print "instance type as follow :\n" + "|".join(typelist)
          sys.exit(1)
    try :
        instancetype = sys.argv[1][2:]
        sdbsize = int(sys.argv[2][2:])
        instancenum = int(sys.argv[3][2:])
        tag = sys.argv[4][2:]
    except Exception ,e:
        print e
        print "command format error"
        sys.exit(1)
    print "instance type is: "+instancetype
    print "sdbsize is: "+str(sdbsize)+" GB"
    print "number of instance is: "+str(instancenum)
    print "tag of instance  is: "+tag
    if instancetype not in typelist:
       print "maybe the instance type in not right, please make sure or get contact to lvzj"
       sys.exit(1)
    awsci= AwsCI(instancetype,sdbsize,instancenum,tag)
    awsci.checkimg()
    print "check imageid is ok"
    awsci.createins()
    print "create instances is ok"
    awsci.printres()
