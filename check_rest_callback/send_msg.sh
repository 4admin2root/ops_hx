#!/bin/bash
timestamp=`date +%s`
echo $timestamp
token=`cat callback_token`
echo $token
clustername=ebs
echo $clustername
postdata={\"target_type\":\"users\",\"target\":\[\"user001\"\],\"msg\":{\"type\":\"txt\",\"msg\":\"timestamp_${timestamp}_clustername_${clustername}\"},\"from\":\"admin\"}
echo $postdata
curl -XPOST "https://a1.easemob.com/easemob-demo/callbacktest/message" -d ${postdata} -H "Authorization:Bearer ${token}"
