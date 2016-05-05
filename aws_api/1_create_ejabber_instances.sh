#!/bin/bash
#create ejabberd instance
dir=`pwd`
gitdir=/home/adminroot/git/easemob-ops/ops-repo
source $dir/config.sh || exit
#python aws_create_ejabberd.py -s ${new_instance_start} -t ${instance_type} -m ${ami_id} -n ${new_instance_num} || exit
#update hosts and inventory file
cd $gitdir && git pull || exit
echo "#add ejabberd auto" >> $gitdir/roles/common/file_hosts/files/hosts.pro4-aws-ca
cat $dir/hosts >> $gitdir/roles/common/file_hosts/files/hosts.pro4-aws-ca
for i in `awk '{print $2}' $dir/hosts`
do
sed -i "s/${ami_hostname}\:3299/&\n${i}\:3299/g" $gitdir/inventory/pro4/pro4-aws-ca.yml
done
grep -A 20 ${ami_hostname} $gitdir/inventory/pro4/pro4-aws-ca.yml
git commit -m 'add ejabberd auto' roles/common/file_hosts/files/hosts.pro4-aws-ca inventory/pro4/pro4-aws-ca.yml
#git push
#ansible-play -i inventory/pro4/pro4-aws-ca.yml playbooks/pro4/hosts.yml
#change hostname for new instances
echo change hostname for new instances
cd $dir
for i in `awk '{print $2}' $dir/hosts`
do
echo $i
ssh -p3299 $i "sudo sed -i \"s/${ami_hostname}/$i/g\" /etc/sysconfig/network " 
ssh -p3299 $i "sudo hostname $i" 
done
#change machineid in ejabberd.yml  for new instances
echo change machineid in ejabberd.yml  for new instances
oid=`echo ${ami_hostname} |egrep '[0-9]+$' -o`
for i in `awk '{print $2}' $dir/hosts`
do
echo $i
id=`echo $i |egrep '[0-9]+$' -o`
echo $id
ssh -p3299 $i " sed -i \"s/machineid\: 6${oid}/machineid\: 6$id/g\" /data/apps/opt/ejabberd/etc/ejabberd/ejabberd.yml " 
ssh -p3299 $i "grep machineid:" /data/apps/opt/ejabberd/etc/ejabberd/ejabberd.yml
done
#change ip and hostname in netrc   for new instances
cat $dir/hosts |while read line
do
ip=`echo $line |awk '{print $1}'`
echo $ip
ipcom=`echo $ip |sed 's/\./,/g'`
echo $ipcom
hostname=`echo $line |awk '{print $2}'`
echo $hostname
ssh -p3299 $hostname "sed \"s/[0-9]{1,3},[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}/${ipcom}/g\" /data/apps/opt/ejabberd/etc/ejabberd/inetrc"
ssh -p3299 $hostname "sed \"s/${ami_hostname}/${hostname}/g\" /data/apps/opt/ejabberd/etc/ejabberd/inetrc"
done
#change ip and hostname in ejabberdctl.cfg   for new instances
cat $dir/hosts |while read line
do
ip=`echo $line |awk '{print $1}'`
echo $ip
hostname=`echo $line |awk '{print $2}'`
echo $hostname
ssh -p3299 $hostname "sed \"s/INET_DIST_INTERFACE=.*$/INET_DIST_INTERFACE=${ip}/g\" /data/apps/opt/ejabberd/etc/ejabberd/ejabberdctl.cfg"
ssh -p3299 $hostname "sed \"s/${ami_hostname}/${hostname}/g\" /data/apps/opt/ejabberd/etc/ejabberd/ejabberdctl.cfg"
done
#delete normal files in /data/apps/opt/ejabberd/var/lib/ejabberd/ for new instances
for i in `awk '{print $2}' $dir/hosts`
do
echo $i
#delete normal files in /data/apps/opt/ejabberd/var/lib/ejabberd/ for new instances
ssh -p3299 $i "rm -rf /data/apps/opt/ejabberd/var/lib/ejabberd/*"
#change hostname in /etc/monitrc  for new instances
ssh -p3299 $i "sudo sed \"s/${ami_hostname}/${i}/g\" /etc/monitrc"
#restart monit  for new instances
ssh -p3299 $i "sudo /etc/init.d/monit restart;"
#start ejabberd  for new instances
ssh -p3299 $i "sudo /etc/init.d/monit restart;"
done
#add ejabberslist  for new instances
#add elb for new instances
#.erlang.hosts
