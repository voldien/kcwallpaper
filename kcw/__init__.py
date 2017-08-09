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
import socket
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

# FQDN for checking internet connection.
REMOTE_SERVER = "google.com"

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
config_set("ssl", True)
config_set("hasInternet", True)
config_set("cacheonly", False)
config_set("wallpaper_fifo", os.path.expanduser("~/.kcw/wallfifo0"))
config_set("config_file", CONFIG_FIELPATH + CONFIG_FIELNAME)
config_set("usecache", DEFAULT_USECACHE)
config_set("cachedata", DEFAULT_CACHEDATA)
config_set("cachedirectory", DEFAULT_CACHEFILEDIRECTORY)
config_set("sql", "sqlite")
config_set("use_sql", DEFAULT_USE_MYSQL)
config_set("sql_database", 'konachan')
config_set("sql_hostname", DEFAULT_MYSQL_HOSTNAME)
config_set("sql_username", DEFAULT_MYSQL_USERNAME)
config_set("sql_password", DEFAULT_MYSQL_PASSWORD)
config_set("sql_port", DEFAULT_MYSQL_PORT)
config_set("sql_table", "img")
config_set("tag", DEFAULT_SEARCHTAG)
config_set("sleep", DEFAULT_SLEEPTIME)
config_set("quality", HIGH_QUALITY)

# Simple wallpaper command line.
swp_args = ["swp", "--fullscreen", "-C"]


def create_cache_directory(directory):
    """
    Create cache directory.
    :param directory: directory path.
    """
    verbose_printf("Creating cache directory %s." % directory)
    try:
        os.makedirs(directory)
    except Exception as err:
        print(err.message)
        exit(1)


def create_popen(cmd):
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


def write_fifo(wallpaper_fifo, pbuf):
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
            errorf("FIFO file didn't exist.\n")
            exit(1)
    except IOError as err:
        errorf("Couldn't open fifo file '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except AttributeError as err:
        errorf("Attribute error '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except Exception as err:
        errorf("Unexpected error:", sys.exc_info()[0])
        exit(1)

    return nbytes


def kcw_connection_wait():
    """
    Wait in till the connection can access internet.
    :return:
    """

    try:
        # Fetch address.
        host = socket.gethostbyname(REMOTE_SERVER)

        # Try connect.
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False
