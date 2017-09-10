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
import abc


class SqlCacheConnection(object):
    """
    Abstract base class for the SQL
    cache implementation.
    """

    def __init__(self):
        self._sql_connection = None
        self._sql_query = self.init_query_commands()

    @abc.abstractmethod
    def execute_command(self, query):
        """
        Execute internal query command.
        :param query: query string.
        :return:
        :rtype: tuple
        """
        pass

    @abc.abstractmethod
    def connect(self, user, password, host, port, database):
        """
        Connect to sql server.
        :param user: username.
        :param password: password
        :param host: host either as Dot-decimal notation or FQDN.
        :param port: port on server.
        :param database: database schema.
        :return: none false if successfully.
        """
        pass

    @abc.abstractmethod
    def disconnect(self):
        """
        Disconnect from server.
        """
        pass

    def get_sqlcon(self):
        """

        :return:
        :rtype: object
        """
        return self._sql_connection

    def set_sqlcon(self, connection):
        """

        :param connection:
        :return:
        """
        self._sql_connection = connection

    @abc.abstractmethod
    def clear_cache(self, table):
        """
        Clear all cache stored on the sql database.
        :param table:
        :return: none false if successfully.
        """
        pass

    @abc.abstractmethod
    def check_table_exists(self, table):
        """
        Check if table exists in sql schema.
        :param table: name of table
        :return: none false if exists.
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def check_img_exists(self, table, imgid):
        """
        Check if image exist in table.
        :param table: table to lookup at.
        :param imgid: image unique ID.
        :return: none false if image exists.
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def num_entries_by_table(self, table):
        """
        Query number of entries in table.
        :param table: table in sql database.
        :return: number of entries.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def add_img_entry(self, table, url, preview, score, imgid, tags):
        """
        Add image to sql.
        :param table:
        :param url:
        :param preview:
        :param score:
        :param imgid:
        :param tags:
        :return: non-false if successful.
        """
        pass

    @abc.abstractmethod
    def get_cached_img_url_by_id(self, table, imgid):
        """
        Get cached image url by image unique ID.
        :param table:
        :param imgid:
        :return: non-empty string.
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def get_cached_img_url_by_tag(self, table, col, tag, offset=0):
        """
        Get cached image local directory path by the tag
        associated with the image.
        :param table: table to search on.
        :param col:
        :param tag: tags associated with image.
        :param offset: nth result.
        :return: non-empty string.
        :rtype: str
        """
        pass

    def get_tag_sql_condition(self, tag):
        """
        Create 'where' condition sequence
        for each of the individual tags.
        :param tag: string with tag separated by whitespace.
        :return: condition string sequence.
        """
        logic = []
        tags = str(tag).split(" ")
        for i in tags:
            logic.append(' tags LIKE \'%{}%\' AND'.format(i))
        else:
            logic[-1] = logic[-1].replace("AND", "")
        return "".join(logic)

    @abc.abstractmethod
    def init_query_commands(self):
        """
        Create query command directory.
        :return: non-empty list.
        :rtype: list
        """
        pass

    def get_querylist(self):
        """
        Get query format list.
        :return: non-empty list.
        :rtype: list
        """
        return self._sql_query

    queryf = property(get_querylist, None)
    connection = property(get_sqlcon, set_sqlcon)

