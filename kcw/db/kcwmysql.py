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
from dbdef import *
import time


class MySqlConnection:
    """"""

    con = None
    enabled = True

    #
    def __init__(self):
        self.con = None
        self.enabled = True

    #
    def kcw_is_mysql_enabled(self):
        return self.enabled

    # Execute SQL command.
    def kcw_mysql_execute_command(self, query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
            res = cur.fetchone()
            cur.close()
            del cur
            return res
        except mysql.connector.Error as err:
            print(err.message)
        except mysql.connector.InternalError as err:
            print(err.message)
        except Exception as err:
            print(err.message)

        return None

    # Connect to mysql server.
    def kcw_sql_connect(self, user, password, host, port, database):
        try:
            self.con = mysql.connector.connect(user=user, password=password,
                                                 host=host,
                                                 database=database)
            return self.con
        except mysql.connector.Error as err:
            print("Couldn't connect to a mysql server %s:%d %s." % (host, port, err.message))
            print("Caching can not be used without MySQL.")
        except Exception as err:
            print("Couldn't connect to mysql, %s." % err.message)
        return None

    #
    def kcw_sql_disconnect(self):
        if self.con is not None:
            self.con.close()

    #
    def kcw_sql_clear_cache(self, table):
        if self.con is None:
            return

        self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_TRUNCATE.format(table))

    # Check if table has been created.
    def kcw_sql_check_table_exists(self, table):
        if not self.kcw_is_mysql_enabled():
            return False

        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_TABLE_EXIST.format(table))

        return res is not None

    #
    def kcw_sql_check_img_exists(self, table, imgid):
        if not self.kcw_is_mysql_enabled():
            return False

        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_CHECK_IMG_EXISTS)
        return res is not None

    #
    def kcw_sql_num_entries_by_table(self, table):
        if not self.kcw_is_mysql_enabled():
            return False

        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_NUM_ENTRIES_IN_TABLE.format(table))

        if res:
            return res[0]
        else:
            return 0

    #
    def kcw_add_img_entry(self, table, url, preview, score, imgid, tags):
        if not self.kcw_is_mysql_enabled():
            return False

        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_ADD_IMG_ENTRY.format(
            table, url, preview, score, imgid, tags, time.time()))

        return res is not None

    #
    def kcw_get_sql_cached_img_url_by_id(self, table, imgid):
        if not self.kcw_is_mysql_enabled():
            return None

        #
        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_IMG_BY_IMGID.format(table, imgid))

        # Check result.
        if res:
            return str(res[0])
        else:
            return None


    def kcw_get_sql_cached_img_url_by_tag(self, table, col, tag, offset=0):
        if not self.kcw_is_mysql_enabled():
            return None

        res = self.kcw_mysql_execute_command(self.con, SQL_FORMAT_QUERY_IMG_BY_TAG.format(col, table, tag, offset))

        # Check result.
        if res:
            return str(res[0])
        else:
            return None
