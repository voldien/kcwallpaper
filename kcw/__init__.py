# script that performs all main logic for kcwallpaper
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
import os
import subprocess

import kcw.kcwreadoptions
from kcwconfiguration import *
from kcwlog import *
from kcwsimpleparser import *

# Global constant variable.
VERSION = "0.9a0"
CONFIG_FIELPATH = "/etc/"
CONFIG_FIELNAME = "kcw.conf"
DEFAULT_CONFIG_PATH = CONFIG_FIELPATH + CONFIG_FIELNAME
DEFAULT_USECACHE = True
DEFAULT_CACHEDATA = True
DEFAULT_CACHEFILEDIRECTORY = os.path.expanduser("~/.kcw/cache")
DEFAULT_SLEEPTIME = 10.0
DEFAULT_SEARCHTAG = "cat"
DEFAULT_USE_MYSQL = True
DEFAULT_SQL_BIN = "mysql"
DEFAULT_MYSQL_PORT = 3389
DEFAULT_MYSQL_HOSTNAME = "localhost"
DEFAULT_MYSQL_USERNAME = "kcwadmin"
DEFAULT_MYSQL_PASSWORD = "randompass"
DEFAULT_MYSQL_DATABASE = "konachan"
kcwdb = "mysql"

# Options mapping.
KONACHAN_SECURITY_FLAG = {False: "-n", True: "-s"}
URL_PROTOCOL_QUALIFIER = {False: "http", True: "https"}

# Supported configuration qualifier.
SUPPORT_CONFIG_QUALIFIER = ["usesql", "sql", "hostname", "port", "db", "username", "password", "sleep", "tag",
                            "cachedata", "usecache", "cachedir", "flag", "fifo", "ssl"]

# Quality enumerator values.
HIGH_QUALITY = 2
MEDIUM_QUALITY = 1
LOW_QUALITY = 0
QUALITY_CONSTANT = {"low": LOW_QUALITY, "medium": MEDIUM_QUALITY, "high": HIGH_QUALITY}
QUALITY_SQL_COLUMN = {LOW_QUALITY: "preview", MEDIUM_QUALITY: "sample", HIGH_QUALITY: "url"}

# Konachan program option arguments.
kc_array_args = ["konachan", "-S", "-f", "\"url sample preview score id tags\"", "-t \"%s\"", "-p %d", "--limit=1"]

# Default initialization config Variables.
kcw_config_set("ssl", True)
kcw_config_set("hasInternet", True)
kcw_config_set("cacheonly", False)
kcw_config_set("wallpaper_fifo", os.path.expanduser("~/.kcw/wallfifo0"))
kcw_config_set("config_file", CONFIG_FIELPATH + CONFIG_FIELNAME)
kcw_config_set("usecache", DEFAULT_USECACHE)
kcw_config_set("cachedata", DEFAULT_CACHEDATA)
kcw_config_set("cachedirectory", DEFAULT_CACHEFILEDIRECTORY)
kcw_config_set("sql", "sqlite")
kcw_config_set("use_sql", DEFAULT_USE_MYSQL)
kcw_config_set("sql_database", 'konachan')
kcw_config_set("sql_hostname", DEFAULT_MYSQL_HOSTNAME)
kcw_config_set("sql_username", DEFAULT_MYSQL_USERNAME)
kcw_config_set("sql_password", DEFAULT_MYSQL_PASSWORD)
kcw_config_set("sql_port", DEFAULT_MYSQL_PORT)
kcw_config_set("sql_table", "img")
kcw_config_set("tag", DEFAULT_SEARCHTAG)
kcw_config_set("sleep", DEFAULT_SLEEPTIME)
kcw_config_set("quality", HIGH_QUALITY)

# Simple wallpaper command line.
swp_args = ["swp", "--fullscreen", "-C"]


def kcw_create_directory(directory):
    """
    Create directory.
    :param directory: directory path.
    """
    kcw_verbose_printf("Creating cache directory %s." % directory)
    try:
        os.makedirs(directory)
    except Exception as err:
        print(err.message)
        exit(1)


def kcw_create_popen(cmd):
    """
    Create piped process.
    :param cmd: program and argument string.
    :return: file if successfully.
    :exception
    """
    try:
        return subprocess.Popen(cmd)
    except Exception as err:
        raise err


def kcw_write_fifo(wallpaper_fifo, pbuf):
    """
    Write to SWP wallpaper program FIFO(First in, First out).
    :param wallpaper_fifo: fifo file path.
    :param pbuf: data buffer.
    :return: number of bytes written.
    """
    nbytes = 0
    try:
        # Check if file still exist.
        if os.path.exists(wallpaper_fifo):
            f = open(wallpaper_fifo, 'wb')
            nbytes = f.write(pbuf)
            f.close()
        else:
            kcw_errorf("FIFO file didn't exist.\n")
            exit(1)
    except IOError as err:
        kcw_errorf("Couldn't open fifo file '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except AttributeError as err:
        kcw_errorf("Attribute error '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except Exception as err:
        kcw_errorf("Unexpected error:", sys.exc_info()[0])
        exit(1)

    return nbytes

