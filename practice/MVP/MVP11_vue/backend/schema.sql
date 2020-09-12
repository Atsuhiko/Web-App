drop table if exists results;
create table results (
  `id` integer primary key autoincrement,
  `filepath` text not null,
  `prediction` text not null,
  `dog` real,
  `cat` real,
  `created` datetime default CURRENT_TIMESTAMP
);