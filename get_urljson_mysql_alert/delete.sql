
use conncount;
delete from getlog where logdt < now() + interval -1 day;
commit;
