#
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
import os.path
import sys
import time

from dbdef import *
from kcw.db.kcwsql import SqlCacheConnection
from kcw.kcwconfiguration import config_get
from kcw.kcwlog import errorf, verbose_printf

#
if sys.version_info[0] < 3:
    import sqlite3
else:
    import _sqlite3 as sqlite3


class SqliteCacheConnection (SqlCacheConnection):
    """
    SQLite is a lightweight sql server that
    does not require any server running.
    """

    def __init__(self):
        self.schema = None
        super(SqliteCacheConnection, self).__init__()

    def execute_command(self, query):
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            self.connection.commit()
            res = cur.fetchone()
            cur.close()
            return res
        except sqlite3.DatabaseError as err:
            errorf("Failed perform query '{}'\n\terror : {}.\n", query, err.message)
            exit(1)
        except Exception as err:
            errorf("Failed perform query '{}'\n\terror : {}.\n", query, err.message)
        return ()

    def connect(self, user, password, host, port, database):
        """
        Connect to mysql server.
        :param user: dummy
        :param password: dummy
        :param host: dummy
        :param port: dummy
        :param database:
        :return:
        """
        try:
            path = "{}/../kcwsqllite.db".format(config_get("cachedirectory"))

            if os.path.exists(path):
                verbose_printf("Loading database at %s" % path)
            else:
                verbose_printf("Created database at %s" % path)

            self.connection = sqlite3.connect(database=path)
            self.schema = database

            self.create_tables()

        except Exception as err:
            errorf(err.message)

    def disconnect(self):
        self.connection.close()

    def create_tables(self):
        self.execute_command(self.queryf[SQL_FORMAT_CREATE_TABLE])

    def clear_cache(self, table):
        self.execute_command(self.queryf[SQL_FORMAT_QUERY_TRUNCATE].format(table))

    def check_table_exists(self, table):

        res = self.execute_command(self.queryf[SQL_FORMAT_QUERY_TABLE_EXIST].format(table))

        return next(iter(res or []), None)

    def check_img_exists(self, table, imgid):

        #
        res = self.execute_command(self.queryf[SQL_FORMAT_QUERY_CHECK_IMG_EXISTS].format(table, imgid))

        return next(iter(res or []), None)

    def num_entries_by_table(self, table):

        res = self.execute_command(self.queryf[SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE].format(table))

        return next(iter(res or []), None)

    def add_img_entry(self, table, url, preview, score, imgid, tags):

        res = self.execute_command(self.queryf[SQL_FORMAT_QUERY_ADD_IMG_ENTRY].format(
            table, url, preview, score, imgid, tags, time.time()))

        return next(iter(res or []), None)

    def get_cached_img_url(self, table):

        res = self.execute_command(self.queryf[SQL_FORMAT_GET_CACHED_IMAGE_URL].format(table, 1))

        return next(iter(res or []), None)

    def get_cached_img_url_by_id(self, table, imgid):

        #
        res = self.execute_command(self.queryf[SQL_FORMAT_QUERY_IMG_BY_IMGID].format(table, imgid))

        return next(iter(res or []), None)

    def get_cached_img_url_by_tag(self, table, col, tag, offset=0):

        res = self.execute_command(
            self.queryf[SQL_FORMAT_QUERY_IMG_BY_TAG].format(col, table, self.get_tag_sql_condition(tag), offset))

        return next(iter(res or []), None)

    def init_query_commands(self):
        """

        :return:
        """
        querylist = []
        querylist.insert(SQL_FORMAT_QUERY_TRUNCATE, "DELETE FROM {} ;")
        querylist.insert(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS, "SELECT COUNT(*) FROM {} WHERE sourceid='{}';")
        querylist.insert(SQL_FORMAT_QUERY_TABLE_EXIST, "")
        querylist.insert(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS, "SELECT COUNT(*) FROM {} WHERE sourceid='{}';")

        querylist.insert(SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE, "SELECT COUNT(*) FROM {} ;")
        querylist.insert(SQL_FORMAT_QUERY_ADD_IMG_ENTRY,
                         "INSERT INTO {} (url, preview, score, sourceid, tags, date) VALUES"
                         "(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');")
        querylist.insert(SQL_FORMAT_GET_CACHED_IMAGE_URL, "SELECT url FROM %s OFFSET %d LIMIT 1 ;")
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

        return querylist
