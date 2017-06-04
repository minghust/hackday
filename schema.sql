drop table if exists item;
create table items(
    id integer primary key autoincrement,
    name text not null,
    chname text not null,
    description text not null
);
