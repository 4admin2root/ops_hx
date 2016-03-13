#!/bin/bash
cd /data/shell/check_rest_callback/
timestamp=`date +%s`
clustername=ebs
echo $timestamp
token=`cat callback_token`
echo $token
echo $clustername
postdata={\"target_type\":\"users\",\"target\":\[\"user001\"\],\"msg\":{\"type\":\"txt\",\"msg\":\"timestamp_${timestamp}_clustername_${clustername}\"},\"from\":\"admin\"}
echo $postdata
curl -m 10 --connect-timeout 3 --retry 2 --retry-delay 1 --retry-max-time 2 -s -XPOST "https://a1.easemob.com/easemob-demo/callbacktest/message" -d ${postdata} -H "Authorization:Bearer ${token}"
dtnow=`date +%H%M`
if [ $dtnow = '0305' ];then
  exit 0
fi
echo sendtimestamp:$timestamp
sleep 60
gettime=`cat /var/log/nginx/access_callback.log |grep ${timestamp}_clustername_$clustername |tail -n 1|egrep '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}' -o`
gettime=`echo $gettime |sed 's/T/ /'`
echo gettime:$gettime
if [ x"${gettime}" = x ];then
echo warning:gettime can not found
exit 1
fi
gettimestamp=`date -d "${gettime}" +%s`
echo gettimestamp:$gettimestamp
timediff=`expr $gettimestamp - $timestamp`
echo timediff:$timediff
if [ $timediff -gt 60 ];then
   exit 1
fi
