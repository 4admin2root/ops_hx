#!/bin/bash
#初始化aws映像AMI，一般要在ejabberd版本更新后执行，将新生成的ami_id保存在config.sh中
dateymd=`date +%Y%m%d%H%M%S`
source ./config.sh
#creae ami
new_ami=`python aws_img.py --${instance_id} --ejabberd${dateymd} |awk -F: '{print $2}'`
#please change ami_id in config.sh to the new one
sed -i "s/ami_id.*$/ami_id=${new_ami}/g" config.sh
cat config.sh
