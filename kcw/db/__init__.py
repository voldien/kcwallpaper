# Konachan wallpaper database.
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
from __future__ import absolute_import
from kcw.db import kcwmysql
from kcw.db import kcwsqlite


def create_sql_cache_connection(db):
    """
    Factory function for creating sql connection.
    :param db: Database type as string.
    :return: object instance of sql connection.
    """
    try:
        if db == "mysql":
            return kcwmysql.MySqlCacheConnection()
        elif db == "sqlite":
            return kcwsqlite.SqliteCacheConnection()
        else:
            raise ValueError("Invalid database")
    except Exception as err:
        raise err

