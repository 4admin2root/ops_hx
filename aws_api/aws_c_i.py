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

instance = ec2.create_instances(
    ImageId='ami-8d668cc9',
    MinCount=1,
    MaxCount=3,
    KeyName='easemob',
#    SecurityGroups=[
#        'vpc-8b49b3ee'
#    ],
    SecurityGroupIds=[
        'sg-a8df07cd'
    ],
#    UserData='string',
    InstanceType='t2.micro',                      ## important 
#    Placement={
#        'AvailabilityZone': 'string',
#        'GroupName': 'string',
#        'Tenancy': 'dedicated',
#        'HostId': 'string',
#        'Affinity': 'string'
#    },
#    KernelId='string',
#    RamdiskId='string',
    BlockDeviceMappings=[
        {
#            'VirtualName': 'string',
            'DeviceName': '/dev/sdb',
            'Ebs': {
                'VolumeSize': 10,
                 #add another 10GB disk ?
                'DeleteOnTermination': True,
                'VolumeType': 'standard',
                 ## in product is gp2
#                'Iops': 123,
                'Encrypted': False
                    },
#            'NoDevice': 'string'
        },
    ],
    Monitoring={
        'Enabled': False
    },
    SubnetId='subnet-330ad756',
    DisableApiTermination= False,
    InstanceInitiatedShutdownBehavior='stop',
    EbsOptimized=False # for test,in product please set true
    IamInstanceProfile={
        'Name': 'create_by_script'
    },
)
print instance
