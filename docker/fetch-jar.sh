#!/bin/bash -x
PKG_NAME=$1
PKG_VER=$2
echo $PKG_VER |grep -i snapshot
if [ $? -eq 0 ];then
   SPKG_VER=`curl -H 'Authorization: Basic xxxxxxxxxxx' -s "http://hk.nexus.op.easemob.com/nexus/service/local/repositories/snapshots/content/com/easemob/usergrid/${PKG_NAME}/maven-metadata.xml" |grep release |awk -F'<|>'  '{print $3}'`
   PKG_VER=$SPKG_VER
   echo $SPKG_VER > snapshot
   PKG_URL="http://hk.nexus.op.easemob.com/nexus/service/local/repositories/snapshots/content/com/easemob/usergrid/${PKG_NAME}/${PKG_VER}/${PKG_NAME}-${PKG_VER}.jar"
else
   PKG_URL="http://hk.nexus.op.easemob.com/nexus/service/local/repositories/releases/content/com/easemob/usergrid/${PKG_NAME}/${PKG_VER}/${PKG_NAME}-${PKG_VER}.jar"
fi
#HTTP_PROXY="{{ http_proxy_server }}"
if [ "$HTTP_PROXY" != "" -a "$HTTP_PROXY" != "None" ]
then
    CURL_OPTS="-s -x $HTTP_PROXY"
else
    CURL_OPTS="-s "
fi

curl -H 'Authorization: Basic xxxxxxxxxxxxxx==' $CURL_OPTS $PKG_URL.md5 -o $PKG_NAME-$PKG_VER.jar.md5

echo "$(cat $PKG_NAME-$PKG_VER.jar.md5)  $PKG_NAME-$PKG_VER.jar" | md5sum -c
IT_MATCHES=$?

if [ 0 -ne $IT_MATCHES ]
then
	curl -H 'Authorization: Basic xxxxxxxx=' $CURL_OPTS $PKG_URL -o $PKG_NAME-$PKG_VER.jar
fi
echo "$(cat $PKG_NAME-$PKG_VER.jar.md5)  $PKG_NAME-$PKG_VER.jar" | md5sum -c || exit
