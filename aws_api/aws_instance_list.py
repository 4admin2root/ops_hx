#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于
.aws/config
.aws/credentials
"""
import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
ec2 = boto3.resource('ec2')

writer = csv.writer(file('aws_instances.csv','w'))
#get instances and volumes
instances_all = ec2.instances.filter()
volumes_all = ec2.volumes.filter()

writer.writerow(['服务器tag','实例id','实例类型','可用区','实例状态','公有ip','私有ip','创建时间'])
for instance in instances_all:
    writer.writerow([instance.tags[0]['Value'],instance.instance_id,instance.instance_type,instance.placement['AvailabilityZone'],instance.state['Name'],instance.public_ip_address,instance.private_ip_address,instance.launch_time])
