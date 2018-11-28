drop table if exists results;
create table results(
    Id INTEGER primary key autoincrement,
    title char(50) not null,
    `data` text not null,
    `img` text not null,
    `created` datetime default CURRENT_TIMESTAMP
);