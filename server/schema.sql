drop table if exists results;
create table results(
    Id INTEGER primary key autoincrement,
    title char(50) not null,
    `data` text not null,
    `img` text not null,
    `created` datetime default CURRENT_TIMESTAMP
);
drop table if exists user_datas;
CREATE TABLE user_datas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name,
    user_password,
    created_at DEFAULT CURRENT_TIMESTAMP
);