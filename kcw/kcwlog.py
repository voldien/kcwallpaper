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
kcw_verbosity = 0

KCW_QUITE = 0
KCW_VERBOSE = 1
KCW_DEBUG = 2


# Set verbosity level of the program.
def kcw_set_verbosity(verbosity):
    global kcw_verbosity
    kcw_verbosity = verbosity


# Check if verbosity is enabled.
def kcw_is_verbose():
    return kcw_verbose


def kcw_enable_verbose():
    global kcw_verbose
    kcw_verbose = True


# Print error.
def kcw_errorf(fmt, **kwargs):
    sys.stderr.write(fmt % kwargs)
#    print(fmt % kwargs, file=sys.stderr, end='\n')


#
def kcw_logf(verbosity, fmt, *kwargs):
    if kcw_verbose <= verbosity:
        print(fmt % kwargs)


# print
def kcw_verbose_print(fmt, *kwargs):
    return kcw_logf(KCW_VERBOSE, fmt, *kwargs)


#
def kcw_debug_printf(fmt, *kwargs):
    return kcw_logf(KCW_QUITE, fmt % kwargs)

