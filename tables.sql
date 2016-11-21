--Dana Hsiao and Brenna Carver
--Final Project
--Creates tables for DormDatabase

drop table if exists dorms;

create table dorms (
	did int not null auto_increment primary key,
	dorm_name varchar(50) not null,
	location enum("East Side", "West Side", "Other") not null,
	INDEX (did)
)
ENGINE = InnoDB;

drop table if exists people;
create table people (
	username varchar(50) not null primary key,
	password varchar(25),
	INDEX (username)
)
ENGINE = InnoDB;

drop table if exists reviews;
create table reviews (
	rid int auto_increment not null primary key,
	did int not null,
	username varchar(50) not null,
	rating int,
	comment varchar(2000),
	INDEX (rid),
	INDEX (did),
	INDEX (username),
	foreign key(did) references dorms(did) on delete cascade,
	foreign key(username) references people(username) on delete cascade
)
ENGINE = InnoDB;
