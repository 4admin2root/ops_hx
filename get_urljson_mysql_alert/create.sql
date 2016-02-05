Create DATABASE IF NOT EXISTS conncount default charset utf8 COLLATE utf8_general_ci; 

use conncount;

create table getlog (
connects VARCHAR(40),
counts INT(10) UNSIGNED,
changes INT(6),
logdt DATETIME); 

create table conn_threshold (
connects VARCHAR(40) not null,
num int(5),
logdt DATETIME);

create table alertlog (
msg VARCHAR(2000),
logdt DATETIME);

create index idx_getlog_dt on getlog(logdt);
