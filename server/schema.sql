drop table if exists results;
create table results(
  ID integer primary key autoincrement,
  UserName text not null,
  UserPassword text not null,
);