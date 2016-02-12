#!/bin/bash
PIDFILE=/tmp/netjson.pid
export PIDFILE
if [ -f $PIDFILE ]; then
kill `cat $PIDFILE`
fi
cd /root/urljson
if [ $? -eq 0 ]; then
/usr/bin/python urlnetjson.py > /tmp/data.json
fi
