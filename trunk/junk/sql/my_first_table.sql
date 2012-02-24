drop table if exists bbox;
create table bbox (xmin REAL, ymin double, asset TEXT);
insert into bbox (xmin,ymin,asset) values (0,1,'trbo');
insert into bbox (xmin,ymin,asset) values (0.5,1.5,'trbo');
.dump
