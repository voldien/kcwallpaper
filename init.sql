#	The mysql is used in order to cache information from konachan.
#	This script will create all the tables needed and mysql user with sufficent amount
#	of permission in order for it to perform as accordingly.



CREATE SCHEMA IF NOT EXISTS `konachan`;
USE konachan;


#	Table for caching image data.
CREATE TABLE IF NOT EXISTS `img` (
	`id` INT NOT NULL AUTO_INCREMENT,	#	ID
	`sourceid` INT NOT NULL,		#	Source ID
	`url` BLOB NOT NULL,			#	Relative URL
	`preview` BLOB NOT NULL,		#	Relative preview URL.
	`score` INT NOT NULL,			#	Score
	`tags` BLOB NOT NULL,			#	tags
	`date` DATE NOT NULL,			#	Date of modification.
	PRIMARY KEY (`id`)
);


#	Future version allowing more interesting pattern of appearing
#CREATE TABLE IF NOT EXISTS `config` (
#	`id` INT NOT NULL AUTO_INCREMENT,		#	
#	`tags` BLOB NOT NULL,				#	
#	`how` ENUM( 'SUCCESSION', 'RANDOM') NOT NULL,	#
#	PRIMARY KEY (`id`)				#
#);



#	Create user to read the img table.
CREATE USER 'kcwadmin'@'%';							#
GRANT SELECT,INSERT,ALTER,DELETE on konachan.img to 'kcwadmin'@'localhost'	#

