#!/bin/bash
echo ===========================
tail -n 10 opslog
dt=`date +%Y-%m-%d" "%H:%M:%S`
echo ===========================
echo $dt
echo "由于内部管理的要求，需要你准确提供以下信息"
hn=`hostname`
arr=(liult dengc hanyn lvzj duhb)
lines=${#arr[*]}
for ((i=0;i<$lines;i++))
do
echo $i:${arr[$i]}
done
read -p "name id:" id
if test -z "$id"
then
echo "内容为空"
exit 1
fi
if [  $lines -le $id ]
then
echo "id错误"
exit 1
fi
name=${arr[$id]}
echo "姓名:"$name
echo "登录此服务器计划操作服务名称简称(例如:rest)"
read -p  ":" app 
if test -z "$app"
then
echo "内容为空"
exit 1
fi
echo "登录此服务器计划操作的内容和目的"
read -p  ":" con 
if test -z "$con" 
then
echo "内容为空"
exit 1
fi
log="$hn|$dt|$name|$app|$con"
echo $log >>opslog
