# verbose.
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

kcw_verbose = False


def kcw_is_verbose():
    return kcw_verbose


def kcw_enable_verbose():
    global kcw_verbose
    kcw_verbose = True


def kcw_verbose_print(cstr):
    if kcw_is_verbose():
        print(cstr)
