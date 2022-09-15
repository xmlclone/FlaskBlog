-- Blog增加star字段
alter table blog add star integer not null default 0;

-- Blog增加html字段, body存放原始文档(比如原始文档是md格式),html字段是转义后的
alter table blog add html text;