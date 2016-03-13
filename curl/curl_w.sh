modify_code=`curl --retry 2 --retry-delay 2 --retry-max-time 2 -o /dev/null -XPUT "http://a1.easemob.com/easemob-demo/chatdemoui/users/chenchaobing" -H "Authorization:Bearer ${token}" -d '{"ci":"modify_test"}' -w "%{http_code}"`
echo modify_code:$modify_code
if [ $modify_code -ne 200 ];then
 exit 1
fi
#get info
getinfo_code=`curl --retry 2 --retry-delay 2 --retry-max-time 2 -o /dev/null -s -XGET "http://a1.easemob.com/easemob-demo/chatdemoui/users/chenchaobing" -H "Authorization:Bearer ${token}" -w "%{http_code}"`
echo getinfo_code:$getinfo_code
if [ $getinfo_code -ne 200 ];then
 exit 1
fi
