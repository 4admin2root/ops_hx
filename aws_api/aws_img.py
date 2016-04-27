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
class AwsImage:
 __version__ = '0.1'
 __author__ = 'lvzj'
 def __init__(self,instanceid,image_name):
      self.ec2 = boto3.resource('ec2')
      self.client = boto3.client('ec2')
      self.instanceid = instanceid
      self.image_name = image_name
#get image id from my ami
 def checkimg(self,imgid):
     try : 
       response = self.client.describe_images(
       ImageIds=[
        imgid,
          ]
       )
       print response
     except Exception,e:
      print e
      print "get imageid failed"
      sys.exit(1)
 def create_image(self):
   try :
    res_image = self.client.create_image(
    #InstanceId='i-da52fb19',
    InstanceId=self.instanceid,
    #Name= 'ami_name0425',
    Name=self.image_name,
    Description='created by aws_img.py',
    NoReboot= True,
    )
    print 'New imageid is:'+res_image['ImageId']
   except Exception,e:
       print e
       print "create instances image error,please check the parameters and error msg above" 
       sys.exit(1)
if __name__ == '__main__':
    if len(sys.argv) < 3:
          print "command format : python scritfilename --instanceid  --imagename "
          print "\texample : python  aws_img.py --i-da52fb19 --ejabberd20160425"
          sys.exit(1)
    try :
        instanceid = sys.argv[1][2:]
        image_name = sys.argv[2][2:]
    except Exception ,e:
        print e
        print "command format error"
        sys.exit(1)
    awsimage=AwsImage(instanceid,image_name)
    awsimage.create_image()
