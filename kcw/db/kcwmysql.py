# script that encapsulate SQL call for kcwallpaper
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

import mysql.connector
import kcw
from kcwsql import *
from dbdef import *
import time


class MySqlCacheConnection (SqlCacheConnection):
    """
    MySQLConnection is a SqlConnection
    that uses MySQL for storing cache data.
    """

    #
    def __init__(self):
        super(MySqlCacheConnection, self).__init__()
        pass

    def execute_command(self, query):
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            res = cur.fetchone()
            cur.close()
            return res
        except mysql.connector.Error as err:
            kcw.errorf("Failed to perform query '{}'\n\terror : {}.\n", query, err.message)
            exit(1)
        return ()

    def connect(self, user, password, host, port, database):
        try:
            self.connection = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except mysql.connector.Error as err:
            print("Couldn't connect to a mysql server %s:%d %s." % (host, port, err.msg))
            print("Caching can not be used without MySQL.")
        except Exception as err:
            print("Couldn't connect to mysql, %s." % err.message)

        raise Exception("Failed to connect.\n")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def clear_cache(self, table):

        self.execute_command(SQL_FORMAT_QUERY_TRUNCATE.format(table))

    def check_table_exists(self, table):

        res = self.execute_command(SQL_FORMAT_QUERY_TABLE_EXIST.format(table))

        return next(iter(res or []), None)

    def check_img_exists(self, table, imgid):

        res = self.execute_command(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS)

        return next(iter(res or []), None)

    def num_entries_by_table(self, table):

        res = self.execute_command(SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE.format(table))

        return next(iter(res or []), None)

    def add_img_entry(self, table, url, preview, score, imgid, tags):

        res = self.execute_command(SQL_FORMAT_QUERY_ADD_IMG_ENTRY.format(
            table, url, preview, score, imgid, tags, time.time()))

        return next(iter(res or []), None)

    def get_cached_img_url_by_id(self, table, imgid):

        res = self.execute_command(SQL_FORMAT_QUERY_IMG_BY_IMGID.format(table, imgid))

        return next(iter(res or []), None)

    def get_cached_img_url_by_tag(self, table, col, tag, offset=0):

        res = self.execute_command(
            SQL_FORMAT_QUERY_IMG_BY_TAG.format(col, table, self.get_tag_sql_condition(tag), offset))

        return next(iter(res or []), None)

    def init_query_commands(self):
        """

        :return:
        :rtype
        """
        querylist = []
        querylist.insert(SQL_FORMAT_QUERY_TRUNCATE, "TRUNCATE TABLE konachan.{} ;")
        querylist.insert(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS, "SELECT COUNT(*) FROM {} WHERE sourceid='{}';")
        querylist.insert(SQL_FORMAT_QUERY_TABLE_EXIST, "")
        querylist.insert(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS, "SELECT COUNT(*) FROM {} WHERE sourceid='{}';")

        querylist.insert(SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE, "SELECT COUNT(*) FROM {} ;")
        querylist.insert(SQL_FORMAT_QUERY_ADD_IMG_ENTRY, "INSERT INTO {} (url, preview, score, sourceid, tags, date) "
                                                         "VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');")
        querylist.insert(SQL_FORMAT_GET_CACHED_IMAGE_URL, "SELECT url FROM %s LIMIT %d 1 ;")
        querylist.insert(SQL_FORMAT_QUERY_IMG_BY_IMGID, "SELECT url FROM {} WHERE sourceid='{}';")
        querylist.insert(SQL_FORMAT_QUERY_IMG_BY_TAG, "SELECT {} FROM {} WHERE {} LIMIT 1 OFFSET {} ;")
        querylist.insert(SQL_FORMAT_CREATE_TABLE, "CREATE TABLE IF NOT EXISTS `img` ("
                                                  "	`sourceid` INT NOT NULL,"
                                                  "	`url` BLOB NOT NULL,"
                                                  "	`preview` BLOB NOT NULL,"
                                                  "	`score` INT NOT NULL,"
                                                  "	`tags` BLOB NOT NULL,"
                                                  "	`date` DATE NOT  NULL,"
                                                  "	`quality` INT"
                                                  ");")
        querylist.insert(SQL_FORMAT_CREATE_DATABASE, "CREATE SCHEMA IF NOT EXISTS `konachan`; USE konachan;")
        querylist.insert(SQL_FORMAT_CREATE_USER, "CREATE USER 'kcwadmin'@'%';"
                                                 "SET PASSWORD for 'kcwadmin'@'localhost' = PASSWORD(\"randompass\");"
                                                 "GRANT SELECT, INSERT, ALTER, DELETE on konachan.img"
                                                 "to 'kcwadmin'@'localhost'")

        return querylist
