#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于如下两个文件
.aws/config
.aws/credentials
统计了主要两种资源 实例 和 卷
其对应关系可用volume_id关联
"""
import datetime
import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
ec2 = boto3.resource('ec2')

t = datetime.datetime.now().strftime('%Y%m%d%H%M')
writeri = csv.writer(file('aws_instances_'+t+'.csv','w'))
writerv = csv.writer(file('aws_volumes_'+t+'.csv','w'))
#get instances and volumes
instances_all = ec2.instances.filter()
volumes_all = ec2.volumes.filter()
#write csv file
writeri.writerow(['服务器tag','实例id','实例类型','可用区','实例状态','公有ip','私有ip','创建时间','卷id'])
for instance in instances_all:
    tag_name=''
    for t in instance.tags:
        if t['Key'] == 'Name':
           tag_name=t['Value']
    row = [tag_name,instance.instance_id,instance.instance_type,instance.placement['AvailabilityZone'],instance.state['Name'],instance.public_ip_address,instance.private_ip_address,instance.launch_time]
    for dev  in instance.block_device_mappings:
      row.append(dev['Ebs']['VolumeId'])
    writeri.writerow(row)

writerv.writerow(['卷id','卷状态','空间大小GB','创建时间','类型'])
for volume in volumes_all:
    writerv.writerow([volume.volume_id,volume.state,volume.size,volume.create_time,volume.volume_type])
