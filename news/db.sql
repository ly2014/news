drop table if exists news;
create table news(
    id int primary key auto_increment,
    title varchar(255) not null,
    publish_date date not null
)charset=utf8;