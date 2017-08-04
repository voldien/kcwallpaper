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
import kcw
import kcw.db
import getopt
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
    :return:
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopt, longoptions)
    except getopt.GetoptError as err:
        print(err.message)
        exit()

    for o, a in opts:
        if o in ("-v", "--version"):
            print("version %s" % kcw.VERSION)
            exit(0)
        elif o in ("-V", "--verbose"):
            kcw.kcw_set_verbosity(kcw.KCW_VERBOSE)
            kcw.kcw_verbose_printf("Enabled verbose.\n")
        elif o in ("-D", "--debug"):
            kcw.kcw_verbose_printf("Enabled verbose.\n")
            kcw.kcw_set_verbosity(kcw.KCW_DEBUG)
        elif o in ("-Q", "--quite"):
            kcw.kcw_set_verbosity(kcw.KCW_QUITE)
        elif o in ("-c", "--config"):
            config_path = str(a)
            kcw.kcw_verbose_printf("config file override to {}.".format(config_path))


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
        raise ValueError("Path is not a file.")

    # Parse configuration file.
    config_table, err = kcw.sp_parse_file(config_path)
    if not config_table and err:
        map(kcw.kcw_errorf, err)
        exit(1)

    # Iterate through all of the attributes.
    for k, v in config_table.iteritems():
        if k not in kcw.SUPPORT_CONFIG_QUALIFIER:
            kcw.kcw_debug_printf("%s is not valid config qualifier.", k)
            continue

        # Check each possible key.
        if k == "usesql":
            kcw.kcw_config_set("usesql", (v == 'True'))
            kcw.kcw_verbose_printf("Using SQL feature.")
        elif k == "sql":
            kcw.kcw_config_set("sql", v)
            kcw.kcw_verbose_printf("Set sql to %s.", v)
        elif k == "hostname":
            kcw.kcw_config_set("hostname", v)
            kcw.kcw_verbose_printf("hostname : {}.".format(v))
        elif k == "port":
            kcw.kcw_config_set("port", v)
            kcw.kcw_verbose_printf("port : {}.".format(v))
        elif k == "db":
            kcw.kcw_config_set("db", v)
            kcw.kcw_verbose_printf("DB set to {}.".format(v))
        elif k == "dbtable":
            kcw.kcw_config_set("sql_table", v)
            kcw.kcw_verbose_printf("table set to {}".format(v))
        elif k == "username":
            username = v
            kcw.kcw_config_set("sql_username", username)
            kcw.kcw_verbose_printf("username : {}.".format(username))
        elif k == "password":
            password = v
            kcw.kcw_config_set("sql_password", password)
            kcw.kcw_verbose_printf("password : {}.".format(password))
        elif k == "sleep":
            kcw.kcw_config_set("sleep", float(v))
            kcw.kcw_verbose_printf("sleep : {} secs.".format(float(v)))
        elif k == "tag":
            tag = v
            kcw.kcw_config_set("tag", tag)
            kcw.kcw_verbose_printf("tag : {}.".format(tag))
        elif k == "cachedata":
            cachedata = (v == 'True')
            kcw.kcw_config_set("cachedata", cachedata)
            kcw.kcw_verbose_printf("Caching status {}.".format(cachedata))
        elif k == "usecache":
            usecache = (v == 'True')
            kcw.kcw_config_set("usecache", usecache)
            kcw.kcw_verbose_printf("Using caching status {}".format(usecache))
        elif k == "cachedir":
            cachedirectory = os.path.expanduser(v)
            kcw.kcw_config_set("cachedirectory", cachedirectory)
            kcw.kcw_verbose_printf("Cache directory set to {}".format(cachedirectory))
        elif k == "flag":
            flag = v
            kcw.kcw_verbose_printf("flag : {}.".format(flag))
        elif k == "fifo":
            wallpaper_fifo = os.path.expanduser(v)
            kcw.kcw_config_set("wallpaper_fifo", wallpaper_fifo)
            kcw.kcw_verbose_printf("Wallpaper fifio set to {}.".format(wallpaper_fifo))
        elif k == "ssl":
            ssl = (v == "True")
            kcw.kcw_verbose_printf("SSL set to {}".format(ssl))
        else:
            print ("%s is not a known configuration attribute.\n" % k)


def kcw_read_options(config_path):
    """
    Read options from user argument.
    :param config_path:
    :return:
    """

    assert config_path

    #
    read_first_pass()

    # print warning.
    if int(sys.version.split()[0].split(".")[2]) < 9:
        print("version 2.7.9 or greater is required for using SSL for urllib2. current %s .\n" % sys.version.split()[0])

    #
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
            kcw.kcw_config_set("tag", a)
            kcw.kcw_verbose_printf("Search tag override to {}.".format(a))
        elif o in ("-T", "--sleep"):
            kcw.kcw_config_set("sleep", float(a))
            kcw.kcw_verbose_printf("Sleep time override to {}.".format(float(a)))
        elif o in "cachedir":
            kcw.kcw_config_set("sleep", os.path.expanduser(a))
            kcw.kcw_verbose_printf("Cache directory override to {}.".format(os.path.expanduser(a)))
        elif o in ("-m", "--sql"):
            kcw.kcw_config_set("sql", a)
        elif o in ("--fifo", "-F"):
            kcw.kcw_config_set("wallpaper_fifo", a)
            kcw.kcw_verbose_printf("FIFO override to {}".format(a))
        elif o in "--ssl":
            kcw.kcw_config_set("ssl", a == "True")
        elif o in "--cacheonly":
            kcw.kcw_config_set("cacheonly", True)
        elif o == "--clear-cache":
            kcw.kcw_verbose_printf("Clearing cache database.\n")
            cachecon = kcw.db.kcw_create_sql(kcw.kcw_config_get("sql"))
            cachecon.connect(
                kcw.kcw_config_get("sql_username"),
                kcw.kcw_config_get("sql_password"),
                kcw.kcw_config_get("sql_hostname"),
                kcw.kcw_config_get("sql_port"),
                kcw.kcw_config_get("sql_database"))
            cachecon.clear_cache(cachecon, kcw.kcw_config_get("table"))
            cachecon.disconnect()
            quit(0)
        elif o == "--clear-cache-img":
            kcw.kcw_verbose_printf("Clearing image cache.\n")
            cachedirectory = kcw.kcw_config_get("cachedir")
            lst = os.listdir(cachedirectory)
            for l in lst:
                kcw.kcw_verbose_printf("Removing file from cache directory %s.\n" % l)
                fpath = "%s/%s" % (cachedirectory, l)
                os.remove(fpath)
            quit(0)
        elif o == "--random":
            kcw.kc_array_args.append("--random")
        elif o in ("--quality", "-q"):
            if a in kcw.QUALITY_CONSTANT.keys():
                kcw.kcw_config_set("quality", kcw.QUALITY_CONSTANT[a])
            else:
                kcw.kcw_config_set("quality", int(a))
                kcw.kcw_verbose_printf("Quality set to %s" % kcw.kcw_config_get("quality"))

        elif o in ("-A", "--advanced_konachan_flag"):
            kcw.kc_array_args.append(a)
        else:
            pass
