#!/usr/bin/python
# -*- coding:utf-8 -*- 

import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    #Filters=[{'Name': 'tag-key', 'Values': ['Name']},{'Name':'tag-value','Values':['pro4-aws-ca-ejabberd28']}])
    #Filters=[{'Name': 'tag:Name=ejabberd'}])
    Filters=[{'Name': 'tag:Name=ejabberd'}])


#volumes = ec2.volumes.filter(
#    Filters=[{'Name': 'status', 'Values': ['in-use']}])
#
for instance in instances:
    print instance.id,instance.tags

