#!/usr/bin/python
# -*- coding:utf-8 -*- 

import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
ec2 = boto3.resource('ec2')

writer = csv.writer(file('aws_instances_all.csv','w'))

#instances = ec2.instances.filter(
#    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

instances_all = ec2.instances.all()
#volumes_all = ec2.volumes.filter()

#volumes = ec2.volumes.filter(
#    Filters=[{'Name': 'status', 'Values': ['in-use']}])
#
writer.writerow(['id','ami_launch_index','architecture', 'block_device_mappings' ,'client_token' ,'ebs_optimized' ,'hypervisor' ,'iam_instance_profile' ,'image_id' ,'instance_id' ,'instance_lifecycle' ,'instance_type' ,'kernel_id' ,'key_name' ,'launch_time' ,'monitoring' ,'network_interfaces_attribute' ,'placement' ,'platform' ,'private_dns_name' ,'private_ip_address' ,'product_codes' ,'public_dns_name' ,'public_ip_address' ,'ramdisk_id' ,'root_device_name' ,'root_device_type' ,'security_groups' ,'source_dest_check' ,'spot_instance_request_id' ,'sriov_net_support' ,'state' ,'state_reason' ,'state_transition_reason' ,'subnet_id' ,'tags' ,'virtualization_type' ,'vpc_id'])
for instance in instances_all:
    writer.writerow([instance.id,instance.ami_launch_index,instance.architecture,instance.block_device_mappings,instance.client_token,instance.ebs_optimized,instance.hypervisor,instance.iam_instance_profile,instance.image_id,instance.instance_id,instance.instance_lifecycle,instance.instance_type,instance.kernel_id,instance.key_name,instance.launch_time,instance.monitoring,instance.network_interfaces_attribute,instance.placement,instance.platform,instance.private_dns_name,instance.private_ip_address,instance.product_codes,instance.public_dns_name,instance.public_ip_address,instance.ramdisk_id,instance.root_device_name,instance.root_device_type,instance.security_groups,instance.source_dest_check,instance.spot_instance_request_id,instance.sriov_net_support,instance.state,instance.state_reason,instance.state_transition_reason,instance.subnet_id,instance.tags,instance.virtualization_type,instance.vpc_id])

