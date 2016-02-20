#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于如下两个文件
.aws/config
.aws/credentials
"""
import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
#get image id from my ami
try : 
 response = client.describe_images(
    ImageIds=[
        'ami-8d668cc9',
    ]
 )
except Exception,e:
     print e
     sys.exit()
print response

instances = ec2.create_instances(
    ImageId='ami-8d668cc9',
    MinCount=1,                             #please change
    MaxCount=3,                             #please change
    KeyName='easemob',
    SecurityGroupIds=[
        'sg-a8df07cd'
    ],
    InstanceType='m3.large',                      ## please change 
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sdb',
            'Ebs': {
                'VolumeSize': 30,                ## please change
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
for instance in instances:
    tag = instance.create_tags(Tags=[{'Key':'Name','Value':'create-by-script'},])
print "create instances as follow:"
print instances
