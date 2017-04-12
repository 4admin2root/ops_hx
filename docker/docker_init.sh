#!/bin/bash
#scp -P3299 /home/easemob/.ssh/id_rsa 10.117.11.99:/home/easemob/.ssh/
source ./im_tag
git init
git pull git@github.com:easemob/Dockerfile.git
echo "100.98.238.117	docker-registry-cn.easemob.com" |sudo tee -a /etc/hosts
sed -i "s/\/im\/rest.*$/\/im\/rest:${REST_TAG}/" docker-compose.yaml
sed -i "s/\/im\/thrift-login.*$/\/im\/thrift-login:${THRIFT_LOGIN_TAG}/" docker-compose.yaml
sed -i "s/\/im\/tools.*$/\/im\/tools:${TOOLS_TAG}/" docker-compose.yaml
sudo service docker start
docker-compose up -d
sed -i 's/\$([^)]*)/localhost/g' init_db.sh
sleep 30
bash -x init_db.sh
