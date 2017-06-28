# Konachan wallpaper database queries.
# Copyright (C) 2017  Valdemar Lindberg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# SQL constant format query format.
SQL_FORMAT_QUERY_TRUNCATE = "TRUNCATE TABLE konachan.{} ;"
SQL_FORMAT_QUERY_CHECK_IMG_EXISTS = "SELECT COUNT(*) FROM {} WHERE sourceid='{}';"
SQL_FORMAT_QUERY_TABLE_EXIST = ""
SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE = "SELECT COUNT(*) FROM {} ;"
SQL_FORMAT_QUERY_ADD_IMG_ENTRY = "INSERT INTO {} (url, preview, score, sourceid, tags, date) VALUES ('{}','{}','{}','{}','{}','{}');"
SQL_FORMAT_GET_CACHED_IMAGE_URL = "SELECT url FROM %s LIMIT %d 1 ;"
SQL_FORMAT_QUERY_IMG_BY_IMGID = "SELECT url FROM {} WHERE sourceid='{}';"
SQL_FORMAT_QUERY_IMG_BY_TAG = "SELECT {} FROM {} WHERE tags LIKE '%{}%' LIMIT 1 OFFSET {} ;"

# SQL query for creating database.
SQL_CREATE_DATABASE = "CREATE SCHEMA IF NOT EXISTS `konachan`;"
"USE konachan;"

# Table for caching image data.
SQL_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS `img` (" \
    "	`sourceid` INT NOT NULL,"                       \
    "	`url` BLOB NOT NULL,"                           \
    "	`preview` BLOB NOT NULL,"                       \
    "	`score` INT NOT NULL,"                          \
    "	`tags` BLOB NOT NULL,"                          \
    "	`date` DATE NOT  NULL,"                         \
    "	`quality` INT"                                  \
    ");"                                                \


# SQL query command for creating user for access rights.
SQL_CREATE_USER = "CREATE USER 'kcwadmin'@'%';"                                         \
    "SET PASSWORD for 'kcwadmin'@'localhost' = PASSWORD(\"randompass\");"               \
    "GRANT SELECT,INSERT,ALTER,DELETE on konachan.img to 'kcwadmin'@'localhost'"        \


