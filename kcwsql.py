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
from kcwverbose import *
use_mysql = False


def kcw_is_mysql_enabled():
    return use_mysql


# Connect to mysql server.
def kcw_sql_connect(user, password, host, port, database, table):
    try:
        sqlcon = mysql.connector.connect(user=user, password=password,
                                         host=host,
                                         database=database)
        num_cached_entries = kcw_sql_num_entries_by_table(sqlcon, table)
        kcw_verbose_print("Connected to mysql server %s:%d.\n" % (host, port))
        kcw_verbose_print("%d number of cached entries.\n" % num_cached_entries)
        return sqlcon
    except mysql.connector.Error as err:
        print("Couldn't connect to a mysql server %s:%d %s." % (host, port, err.message))
        print("Caching can not be used without MySQL.")
    except Exception as err:
        print("Couldn't connect to mysql, %s." % err.message)
    return None


def kcw_sql_clear_cache(sqlcon, table):
    if sqlcon is None:
        return

    try:
        cursor = sqlcon.cursor()
        query = "TRUNCATE TABLE konachan.{} ;".format(table)
        kcw_verbose_print("Clearing mysql database.\n")
        cursor.execute(query)
        sqlcon.commit()
        cursor.close()
        del cursor
    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.InternalError as err:
        print(err.message)


def kcw_sql_check_table_exists(sqlcon, table):
    if sqlcon is None or kcw_is_mysql_enabled():
        return False

    try:
        cursor = sqlcon.cursor()

    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.InternalError as err:
        print(err.message)

    return True


def kcw_sql_check_img_exists(sqlcon, table, imgid):
    if sqlcon is None or kcw_is_mysql_enabled():
        return False
    res = False
    try:
        cursor = sqlcon.cursor()
        query = "SELECT COUNT(*) FROM {} WHERE sourceid='{}';".format(table, imgid)
        cursor.execute(query)
        res = cursor.fetchone()[0]
        cursor.close()
    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.InternalError as err:
        print(err.message)

    return bool(res)


def kcw_sql_num_entries_by_table(sqlcon, table):
    if sqlcon is None or kcw_is_mysql_enabled():
        return False

    try:
        cursor = sqlcon.cursor()
        query = "SELECT COUNT(*) FROM {} ;".format(table)
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.InternalError as err:
        print(err.message)

    return 0


def kcw_add_img_entry(sqlcon, table, url, preview, score, imgid, tags):

    if sqlcon is None or kcw_is_mysql_enabled():
        return False

    query = "INSERT INTO {} (url,preview,score,sourceid,tags) VALUES ('{}','{}','{}','{}','{}');".format(
        table, url, preview, score, imgid, tags)
    try:
        cursor = sqlcon.cursor()
        cursor.execute(query)
        sqlcon.commit()
        cursor.close()
        del cursor
    except mysql.connector.Error as err:
        print(err.message)


def kcw_get_sql_cached_img_url(sqlcon, table):
    cursor = sqlcon.cursor()
    query = "SELECT url FROM %s LIMIT %d 1 ;".format(table, 1)
    cursor.execute(query)
    cursor.fetchall()
    cursor.close()

    return ""


def kcw_get_sql_cached_img_url_by_id(sqlcon, table, imgid):
    if sqlcon is None or kcw_is_mysql_enabled():
        return ""

    res = {}
    cursor = sqlcon.cursor()
    query = "SELECT url FROM {} WHERE sourceid='{}';".format(table, imgid)
    try:
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        del cursor
    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.errors.InternalError as err:
        print(err.message)

    return str(res[0])


def kcw_get_sql_cached_img_url_by_tag(sqlcon, table, tag):
    if sqlcon is None or kcw_is_mysql_enabled():
        return ""

    cursor = sqlcon.cursor()
    query = "SELECT url FROM {} WHERE LIKE tags='{}';".format(table, tag)
    try:
        cursor.execute(query)
        res = cursor.fetchone()
        cursor.close()
        del cursor
    except mysql.connector.Error as err:
        print(err.message)
    except mysql.connector.errors.InternalError as err:
        print(err.message)

    return str(res[0])
