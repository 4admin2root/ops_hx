#!/usr/bin/python
"""
created by lvzj

please change the variables :
qy_access_key_id
qy_secret_access_key
"""
import datetime
import time
import base64
import hmac
import urllib
from hashlib import sha256

qy_access_key_id = 'xxxxxxxxxxxxxxx'
qy_secret_access_key='xxxxxxxxxxxx'
qytime = time.strftime("%Y-%m-%dT%H:%M:%SZ")
print qytime
qing = {
  "access_key_id":qy_access_key_id,
  "action":"CaptureInstance",
  "instance":"i-wvfkumjx",
  "image_name":"CreatedbyAPI",
  "signature_method":"HmacSHA256",
  "signature_version":1,
  "time_stamp":qytime,
  "version":1,
  "zone":"pek3a"
}
qingsort = []
keys = qing.keys()
keys.sort()
for key in keys:
   a={key:qing[key]}
   qingsort.append(a)
string_to_access = 'https://api.qingcloud.com/iaas/?'
string_to_sign = 'GET\n/iaas/\n'
for i in qingsort :
      string_to_sign += urllib.urlencode(i)
      string_to_sign += '&' 
      string_to_access += urllib.urlencode(i)
      string_to_access += '&'
string_to_sign = string_to_sign[:-1]
h = hmac.new(qy_secret_access_key, digestmod=sha256)
h.update(string_to_sign)
sign = base64.b64encode(h.digest()).strip()
signature = urllib.quote_plus(sign)
string_to_access += 'signature='
string_to_access += signature
print string_to_access
