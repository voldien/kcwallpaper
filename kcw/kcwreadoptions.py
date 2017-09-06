# konachan wallpaper read option script.
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
from . import get_version
from _kcw import SUPPORT_CONFIG_QUALIFIER, kc_array_args, QUALITY_CONSTANT
from kcwsimpleparser import sp_parse_file
from kcwconfiguration import config_set, config_get
from kcwlog import *

import db
import getopt
import argparse
import sys
import os

# getopt short options.
shortopt = "vVDmdt:T:h:P:p:c:F:s:rq:Q"

# getopt long options.
longoptions = ["version", "verbose", "debug", "quite", "tag=", "sleep=", "sql=", "config=", "cachedir=", "fifo=",
               "clear-cache", "clear-cache-img", "ssl", "random", "quality=", "advanced_konachan_flag=", "cacheonly"]


def read_first_pass():
    """
    Read first option pass.
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longoptions)
    except getopt.GetoptError as err:
        errorf(err.message)
        exit(1)

    for o, a in opts:
        if o in ("-v", "--version"):
            print("version %s" % get_version())
            exit(0)
        elif o in ("-V", "--verbose"):
            set_verbosity(KCW_VERBOSE)
            verbose_printf("Enabled verbose.\n")
        elif o in ("-D", "--debug"):
            verbose_printf("Enabled verbose.\n")
            set_verbosity(KCW_DEBUG)
        elif o in ("-Q", "--quite"):
            set_verbosity(KCW_QUITE)
        elif o in ("-c", "--config"):
            config_path = str(a)
            verbose_printf("config file override to {}.".format(config_path))


def read_config_file(config_path):
    """
    Read configuration file
    :param config_path:
    :return:
    """

    # Check if invalid path.
    if not config_path:
        raise ValueError("Invalid path.")

    # Check if path is invalid.
    if not os.path.isfile(config_path):
        raise ValueError("Configuration file path is not a file.")

    # Parse configuration file.
    config_table, err = sp_parse_file(config_path)
    if not config_table and err:
        map(errorf, err)
        exit(1)

    # Iterate through all of the attributes.
    for k, v in config_table.iteritems():
        if k not in SUPPORT_CONFIG_QUALIFIER:
            debug_printf("%s is not valid config qualifier.", k)
            continue

        # Check each possible key.
        if k == "usesql":
            config_set("usesql", (v == 'True'))
            verbose_printf("Using SQL feature.")
        elif k == "sql":
            config_set("sql", v)
            verbose_printf("Set sql to %s.", v)
        elif k == "hostname":
            config_set("hostname", v)
            verbose_printf("hostname : {}.".format(v))
        elif k == "port":
            config_set("port", v)
            verbose_printf("port : {}.".format(v))
        elif k == "db":
            config_set("db", v)
            verbose_printf("DB set to {}.".format(v))
        elif k == "dbtable":
            config_set("sql_table", v)
            verbose_printf("table set to {}".format(v))
        elif k == "username":
            username = v
            config_set("sql_username", username)
            verbose_printf("username : {}.".format(username))
        elif k == "password":
            password = v
            config_set("sql_password", password)
            verbose_printf("password : {}.".format(password))
        elif k == "sleep":
            config_set("sleep", float(v))
            verbose_printf("sleep : {} secs.".format(float(v)))
        elif k == "tag":
            tag = v
            config_set("tag", tag)
            verbose_printf("tag : {}.".format(tag))
        elif k == "cachedata":
            cachedata = (v == 'True')
            config_set("cachedata", cachedata)
            verbose_printf("Caching status {}.".format(cachedata))
        elif k == "usecache":
            usecache = (v == 'True')
            config_set("usecache", usecache)
            verbose_printf("Using caching status {}".format(usecache))
        elif k == "cachedir":
            cachedirectory = os.path.expanduser(v)
            config_set("cachedirectory", cachedirectory)
            verbose_printf("Cache directory set to {}".format(cachedirectory))
        elif k == "flag":
            flag = v
            verbose_printf("flag : {}.".format(flag))
        elif k == "fifo":
            wallpaper_fifo = os.path.expanduser(v)
            config_set("wallpaper_fifo", wallpaper_fifo)
            verbose_printf("Wallpaper fifio set to {}.".format(wallpaper_fifo))
        elif k == "ssl":
            ssl = (v == "True")
            verbose_printf("SSL set to {}".format(ssl))
        else:
            print ("%s is not a known configuration attribute.\n" % k)


def read_options(config_path):
    """
    Read options from user argument.
    :param config_path:
    :return:
    """

    assert config_path

    # Read first argument pass.
    read_first_pass()

    # Read configuration file.
    read_config_file(config_path)

    # Read user input
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longoptions)
    except getopt.GetoptError as err:
        print(err.msg)
        exit()

    # Iterate through each option.
    for o, a in opts:
        if o in ("-t", "--tag"):
            config_set("tag", a)
            verbose_printf("Search tag override to {}.".format(a))
        elif o in ("-T", "--sleep"):
            config_set("sleep", float(a))
            verbose_printf("Sleep time override to {}.".format(float(a)))
        elif o in "cachedir":
            config_set("cachedirectory", os.path.expanduser(a))
            verbose_printf("Cache directory override to {}.".format(os.path.expanduser(a)))
        elif o in ("-m", "--sql"):
            config_set("sql", a)
        elif o in ("--fifo", "-F"):
            config_set("wallpaper_fifo", a)
            verbose_printf("FIFO override to {}".format(a))
        elif o in "--ssl":
            config_set("ssl", a == "True")
        elif o in "--cacheonly":
            config_set("cacheonly", True)
        elif o == "--clear-cache":
            verbose_printf("Clearing cache database.\n")
            cachecon = db.create_sql_cache_connection(config_get("sql"))
            cachecon.connect(
                config_get("sql_username"),
                config_get("sql_password"),
                config_get("sql_hostname"),
                config_get("sql_port"),
                config_get("sql_database"))
            cachecon.clear_cache(config_get("sql_table"))
            cachecon.disconnect()
            quit(0)
        elif o == "--clear-cache-img":
            verbose_printf("Clearing image cache.\n")
            cachedirectory = config_get("cachedirectory")
            lst = os.listdir(cachedirectory)
            for l in lst:
                verbose_printf("Removing file from cache directory %s.\n" % l)
                fpath = "%s/%s" % (cachedirectory, l)
                os.remove(fpath)
            quit(0)
        elif o == "--random":
            kc_array_args.append("--random")
        elif o in ("--quality", "-q"):
            if a in QUALITY_CONSTANT.keys():
                config_set("quality", QUALITY_CONSTANT[a])
            else:
                config_set("quality", int(a))
                verbose_printf("Quality set to %s" % config_get("quality"))

        elif o in ("-A", "--advanced_konachan_flag"):
            kc_array_args.append(a)
        else:
            pass
