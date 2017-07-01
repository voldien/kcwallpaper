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
import sqlite3
import time
import os.path

from dbdef import *
import kcw.kcwconfiguration
from kcw.db.kcwsql import SqlConnection


class SqliteConnection (SqlConnection):
    """ """

    con = None
    enabled = True
    schema = None

    #
    def __init__(self):
        self.con = None
        self.enabled = True

    #
    def is_enabled(self):
        return self.enabled

    # Execute SQL command.
    def kcw_sqlite_execute_command(self, query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
            self.con.commit()
            res = cur.fetchone()
            cur.close()
            del cur
            return res
        except Exception as err:
            print(err.message)
            print(query)

        return None

    # Connect to mysql server.
    def connect(self, user, password, host, port, database):
        """

        :param user: dummy
        :param password: dummy
        :param host: dummy
        :param port: dummy
        :param database:
        :return:
        """
        try:
            path = "%s/kcwsqllite.db" % os.path.expanduser("~/.kcw")
            #kcw.kcwconfiguration.kcw_config_get("cachedirectory")
            #

            if os.path.exists(path):
                kcw.kcw_verbose_print("Loading database at %s" % path)
            else:
                kcw.kcw_verbose_print("Created database at %s" % path)
            self.con = sqlite3.connect(database=path)



            self.schema = database

            #if not self.kcw_sql_check_table_exists(table):
            self.create_tables()

            return self.con
        except Exception as err:
            print(err.message)
            return None

    #
    def disconnect(self):
        self.con.close()

    #
    def create_tables(self):
        self.kcw_sqlite_execute_command(SQL_CREATE_TABLE)

    #
    def clear_cache(self, table):
        self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_TRUNCATE.format(table))

    #
    def check_table_exists(self, table):
        if not self.is_enabled():
            return False

        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_TABLE_EXIST.format(table))

        return res is not None

    #
    def check_img_exists(self, table, imgid):
        if not self.is_enabled():
            return False

        #
        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_CHECK_IMG_EXISTS.format(table, imgid))

        return not(res[0] == 0)

    #
    def num_entries_by_table(self, table):
        if not self.is_enabled():
            return False

        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE.format(table))

        if res:
            return res[0]
        else:
            return 0

    #
    def add_img_entry(self, table, url, preview, score, imgid, tags):
        if not self.is_enabled():
            return False

        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_ADD_IMG_ENTRY.format(
            table, url, preview, score, imgid, tags, time.time()))

        return res is not None

    #
    def get_cached_img_url(self, table):
        cursor = self.con.cursor()
        query = "SELECT url FROM %s LIMIT %d 1 OFFSET 0;".format(table, 1)
        cursor.execute(query)
        cursor.fetchall()
        cursor.close()
        return ""

    #
    def get_cached_img_url_by_id(self, table, imgid):
        if not self.is_enabled():
            return ""

        #
        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_IMG_BY_IMGID.format(table, imgid))

        # Check result.
        if res:
            return str(res[0])
        else:
            return None

    #
    def get_cached_img_url_by_tag(self, table, col, tag, offset=0):
        if not self.is_enabled():
            return ""

        res = self.kcw_sqlite_execute_command(SQL_FORMAT_QUERY_IMG_BY_TAG.format(col, table, tag, offset))

        # Check result.
        if res:
            return str(res[0])
        else:
            return None
