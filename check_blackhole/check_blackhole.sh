#!/bin/bash
##created by lvzj
source /home/easemob/.bash_profile
year=`date +%Y`
logdir=/data/apps/log/ejabberd/check_blackhole/$year
if [ ! -d $logdir ];then
mkdir -p $logdir
fi
cd /data/apps/opt/shell/check_blackhole
if [ $? -eq 0 ];then
  if [ $2 == "all" ];then
./nodetool -sname ejabberd@${1} -setcookie xxxxxx is_blackhole.erl > $logdir/$1_all.out
  elif [ $2 == "muc" ];then
./nodetool -sname ejabberd@${1} -setcookie xxxxxx is_blackhole_muc.erl > $logdir/$1_muc.out
 else
  exit 1
  fi
fi
