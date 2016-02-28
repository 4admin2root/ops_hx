#!/bin/bash
#零点时间 日志切换 忽略检查1次
export LANG="en_US.UTF-8"
dtnow=`date +%H%M%S`
if [ $dtnow = '000000' ];then
  exit 0
fi
echo $dtnow
timestamp=`date +%s`
echo $timestamp
getdt=`tail -n 1 /var/log/nginx/access_callback.log |egrep -o 'timestamp_[0-9]+_clustername_\w+' |tee last_callback|awk -F '_' '{print $2}'`
echo $getdt
timediff=`expr $timestamp - $getdt`
echo $timediff
if [ $timediff -gt 60 ];then
   echo callback timediff is more than 60
   exit 1
fi
