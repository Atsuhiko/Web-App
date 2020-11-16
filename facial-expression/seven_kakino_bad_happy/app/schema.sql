drop table if exists results;
create table results (
  `id` integer primary key autoincrement,
  `filepath` text not null,
  `bad` float not null,
  `happy` float not null,
  `created` datetime default CURRENT_TIMESTAMP
);

