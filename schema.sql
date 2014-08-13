drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    parent_id, integer,
    title text not null,
    text text not null,
    upload text
);
