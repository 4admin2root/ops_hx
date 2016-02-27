#!/bin/bash
#created by lvzj
source /home/easemob/.bash_profile
year=`date +%Y`
logdir=/data/apps/log/ejabberd/check_blackhole/$year
dtnow=`date +%s`
all_stat=''
muc_stat=''
if [ ! -d $logdir ];then
mkdir -p $logdir
fi
cd $logdir
sleep 30
if [ $? -eq 0 ];then
all_no_num=`grep no: --no-filename -c *all.out | awk '{sum+=$1} END {print sum}'`
all_yes_num=`grep yes: --no-filename -c *all.out | awk '{sum+=$1} END {print sum}'`
muc_no_num=`grep no: --no-filename -c *muc.out | awk '{sum+=$1} END {print sum}'`
muc_yes_num=`grep yes: --no-filename -c *muc.out | awk '{sum+=$1} END {print sum}'`
echo timestamp:$dtnow > this.res
echo all_no_num:$all_no_num >> this.res
echo all_yes_num:$all_yes_num >> this.res
echo muc_no_num:$muc_no_num >> this.res
echo muc_yes_num:$muc_yes_num >> this.res
 if [ $all_yes_num -gt 0 ];then
           all_res=yes
      else
         all_res=no
 fi
 if [ $muc_yes_num -gt 0 ];then
           muc_res=yes
      else
         muc_res=no
 fi
else 
   exit 1
fi
if [ ! -f $logdir/report_blackhole_all.res ];then
    echo $dtnow,$all_res,$all_no_num,$all_yes_num >> $logdir/report_blackhole_all.res
 else
    last_all_res=`tail -n 1 $logdir/report_blackhole_all.res|awk -F , '{print $2}'`
    if [ $all_res != $last_all_res ];then
     echo $dtnow,$all_res,$all_no_num,$all_yes_num >> $logdir/report_blackhole_all.res
    fi   
fi
if [ ! -f $logdir/report_blackhole_muc.res ];then
    echo $dtnow,$muc_res,$muc_no_num,$muc_yes_num >> $logdir/report_blackhole_muc.res
 else
    last_muc_res=`tail -n 1 $logdir/report_blackhole_muc.res|awk -F , '{print $2}'`
    if [ $muc_res != $last_muc_res ];then
     echo $dtnow,$muc_res,$muc_no_num,$muc_yes_num >> $logdir/report_blackhole_muc.res
    fi

fi
