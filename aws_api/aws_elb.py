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
import types
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf8') 
class AwsElb:
 __version__ = '0.1'
 __author__ = 'lvzj'
 def __init__(self):
      self.client = boto3.client('elb')
 def deregelb(self,elb,insid):
     try : 
       response = self.client.deregister_instances_from_load_balancer(LoadBalancerName=elb,Instances=[{'InstanceId':insid},])
       if response['ResponseMetadata']['HTTPStatusCode'] == 200 :
          print "del instance from elb:ok"
     except Exception,e:
      print e
      sys.exit(1)
 def regelb(self,elb,insid):
     try : 
       response = self.client.register_instances_with_load_balancer(LoadBalancerName=elb,Instances=[{'InstanceId':insid},])
       if response['ResponseMetadata']['HTTPStatusCode'] == 200 :
          print "add instance to elb:ok"
     except Exception,e:
      print e
      sys.exit(1)
 def printelb(self):
     ec2_client = boto3.client('ec2')
     try : 
       response = self.client.describe_load_balancers()
       for i in response['LoadBalancerDescriptions']:
           print "================"
           print "elbname :"+i['LoadBalancerName']
           print "dnsname :"+i['DNSName']
           print "instanceids :"
           l_ids=[]
           for iid in i['Instances'] :
               l_ids.append(iid['InstanceId'])
           if len(l_ids) == 0 :
              continue
           ec2_response = ec2_client.describe_instances(InstanceIds=l_ids)
           instanceid = ''
           instancename = ''
           instanceip = ''
           for r in ec2_response['Reservations']:
              for instance in r['Instances']:
                 instanceid = instance['InstanceId'] 
                 instanceip = instance['PrivateIpAddress'] 
                 for tag in instance['Tags']:
                    if tag['Key']=='Name':
                      instancename=tag['Value']
                 print instanceid+'|'+instancename+'|'+instanceip
     except Exception,e:
      print e
      sys.exit(1)
if __name__ == '__main__':
    parser = OptionParser(
        usage="""usage:%prog [options] arg
      for example:  python aws_elb.py -e test -i i-xxxxx -a
               """, version="%prog 0.2")
    parser.add_option(
        "-e", "--elb", dest="elb", type="string", help="elb")
    parser.add_option(
        "-i", "--insid", dest="insid", type="string", help="instance id")
    parser.add_option(
        "-l", "--list", action="store_true",dest="list",  help=" list all elbs")
    parser.add_option(
        "-a", "--add", action="store_true",dest="addi",  help=" add instance to elb")
    parser.add_option(
        "-d", "--del", action="store_true",dest="deli",  help=" del instance from  elb")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error(' number of args is not right')
        sys.exit(1)
    awselb=AwsElb()
    if options.list == True :
        awselb.printelb()
    if types.NoneType not in [type(options.elb),type(options.insid)]:
        if options.addi == True:
           awselb.regelb(options.elb,options.insid)
        if options.deli == True:
           awselb.deregelb(options.elb,options.insid)
