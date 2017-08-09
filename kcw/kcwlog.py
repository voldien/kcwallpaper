# logging.
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

import sys

# Verbosity level.
KCW_QUITE = 0
KCW_VERBOSE = 1
KCW_DEBUG = 2

# Verbosity level.
kcw_verbosity = KCW_QUITE


def set_verbosity(verbosity):
    """
    Set logging verbosity level. The higher the
    more information gets logged.
    :param verbosity:
    :return:
    """
    global kcw_verbosity
    kcw_verbosity = verbosity


def get_verbosity():
    """
    Get current verbosity level of the program
    :return: verbosity level as int.
    """
    global kcw_verbosity
    return kcw_verbosity


def errorf(fmt, *kwargs):
    """
    Print error format. The string will be written
    into stderr rather than the default with print.
    :param fmt: format string.
    :param kwargs: list of arguments
    :return: number of character written.
    """
    return sys.stderr.write(fmt.format(*kwargs))


def logf(verbosity, fmt, *kwargs):
    """
    Log format message based on the verbosity.
    :param verbosity: verbosity of the message.
    :param fmt: format message.
    :param kwargs: argument for fmt.
    :return:
    """
    nchar = 0
    if get_verbosity() >= verbosity:
        log = fmt.format(*kwargs)
        nchar = len(log)
        print(log)

    return nchar


def verbose_printf(fmt, *kwargs):
    """
    Verbose logging.
    :param fmt:
    :param kwargs:
    :return: number of character.
    """
    return logf(KCW_VERBOSE, fmt, *kwargs)


def warning_printf(fmt, *kwargs):
    """

    :param fmt:
    :param kwargs:
    :return:
    """
    print(fmt.format(*kwargs))


def debug_printf(fmt, *kwargs):
    """
    Debug logging.
    :param fmt:
    :param kwargs:
    :return: number of character.
    """
    return logf(KCW_DEBUG, fmt, *kwargs)

