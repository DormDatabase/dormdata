--Dana Hsiao and Brenna Carver
--Final Project
--Creates tables for DormDatabase

drop table if exists dorms;

create table dorms (
	did int not null auto_increment,
	dorm_name varchar(50) not null,
	location emum("East Side", "West Side", "Other") not null,
	INDEX (did),
	primary key (did)
)
ENGINE = InnoDB;

drop table if exists reviews;
create table reviews (
	rid int auto_increment not null primary key,
	did int not null,
	username = varchar(50) not null,
	rating int,
	comment varchar(2000),
	foreign key(did) references dorms on delete set null,
	foreign key(username) references people on delete set null
)
ENGINE = InnoDB;

drop table if exists people;
create table people (
	username varchar(50) not null primary key,
	password varchar(25);
)
ENGINE = InnoDB;
