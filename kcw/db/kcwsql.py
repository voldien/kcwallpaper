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

class SqlConnection:
    """"""

#    con = None
#    enabled = True

    #
    def __init__(self):
        pass

    #
    def is_enabled(self):
        pass

    # Execute SQL command.
    def kcw_mysql_execute_command(self, query):
        pass

    # Connect to mysql server.
    def connect(self, user, password, host, port, database):
        pass

    #
    def disconnect(self):
        pass
    #
    def clear_cache(self, table):
        pass

    # Check if table has been created.
    def check_table_exists(self, table):
        pass

    def check_img_exists(self, table, imgid):
        pass

    def num_entries_by_table(self, table):
        pass

    def add_img_entry(self, table, url, preview, score, imgid, tags):
        pass

    def get_cached_img_url_by_id(self, table, imgid):
        pass

    def get_cached_img_url_by_tag(self, table, col, tag, offset=0):
        pass

