#!/bin/bash
PIDFILE=/tmp/Connalert.pid
export PIDFILE
if [ -f $PIDFILE ]; then
kill `cat $PIDFILE`
fi
cd /root/urljson
if [ $? -eq 0 ]; then
/usr/bin/python Connalert.py
fi
