#!/usr/bin/python
# -*- coding:utf-8 -*- 
"""
脚本主要使用了boto3模块,其配置还依赖于如下两个文件
.aws/config
.aws/credentials
统计了RDS instance
"""
import boto3
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8') 
client = boto3.client('rds')
writer = csv.writer(file('aws_rds.csv','w'))
#get rds instances 
#write csv file
writer.writerow(['PubliclyAccessible','MasterUsername','MonitoringInterval','LicenseModel','VpcSecurityGroups','InstanceCreateTime','CopyTagsToSnapshot','OptionGroupMemberships','PendingModifiedValues','Engine','MultiAZ','LatestRestorableTime','DBSecurityGroups','DBParameterGroups','AutoMinorVersionUpgrade','PreferredBackupWindow','DBSubnetGroup','SecondaryAvailabilityZone','ReadReplicaDBInstanceIdentifiers','AllocatedStorage','BackupRetentionPeriod','DBName','PreferredMaintenanceWindow','Endpoint','DBInstanceStatus','EngineVersion','AvailabilityZone','StorageType','DbiResourceId','CACertificateIdentifier','StorageEncrypted','DBInstanceClass','DbInstancePort','DBInstanceIdentifier'])
response = client.describe_db_instances()
reslist = response['DBInstances']
for res in reslist :
       writer.writerow([res['PubliclyAccessible'],res['MasterUsername'],res['MonitoringInterval'],res['LicenseModel'],res['VpcSecurityGroups'],res['InstanceCreateTime'],res['CopyTagsToSnapshot'],res['OptionGroupMemberships'],res['PendingModifiedValues'],res['Engine'],res['MultiAZ'],res['LatestRestorableTime'],res['DBSecurityGroups'],res['DBParameterGroups'],res['AutoMinorVersionUpgrade'],res['PreferredBackupWindow'],res['DBSubnetGroup'],res['SecondaryAvailabilityZone'],res['ReadReplicaDBInstanceIdentifiers'],res['AllocatedStorage'],res['BackupRetentionPeriod'],res['DBName'],res['PreferredMaintenanceWindow'],res['Endpoint'],res['DBInstanceStatus'],res['EngineVersion'],res['AvailabilityZone'],res['StorageType'],res['DbiResourceId'],res['CACertificateIdentifier'],res['StorageEncrypted'],res['DBInstanceClass'],res['DbInstancePort'],res['DBInstanceIdentifier']])
