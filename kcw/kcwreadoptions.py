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
        kcw.errorf(err.message)
        exit()

    for o, a in opts:
        if o in ("-v", "--version"):
            print("version %s" % kcw.VERSION)
            exit(0)
        elif o in ("-V", "--verbose"):
            kcw.set_verbosity(kcw.KCW_VERBOSE)
            kcw.verbose_printf("Enabled verbose.\n")
        elif o in ("-D", "--debug"):
            kcw.verbose_printf("Enabled verbose.\n")
            kcw.set_verbosity(kcw.KCW_DEBUG)
        elif o in ("-Q", "--quite"):
            kcw.set_verbosity(kcw.KCW_QUITE)
        elif o in ("-c", "--config"):
            config_path = str(a)
            kcw.verbose_printf("config file override to {}.".format(config_path))


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
    config_table, err = kcw.sp_parse_file(config_path)
    if not config_table and err:
        map(kcw.errorf, err)
        exit(1)

    # Iterate through all of the attributes.
    for k, v in config_table.iteritems():
        if k not in kcw.SUPPORT_CONFIG_QUALIFIER:
            kcw.debug_printf("%s is not valid config qualifier.", k)
            continue

        # Check each possible key.
        if k == "usesql":
            kcw.config_set("usesql", (v == 'True'))
            kcw.verbose_printf("Using SQL feature.")
        elif k == "sql":
            kcw.config_set("sql", v)
            kcw.verbose_printf("Set sql to %s.", v)
        elif k == "hostname":
            kcw.config_set("hostname", v)
            kcw.verbose_printf("hostname : {}.".format(v))
        elif k == "port":
            kcw.config_set("port", v)
            kcw.verbose_printf("port : {}.".format(v))
        elif k == "db":
            kcw.config_set("db", v)
            kcw.verbose_printf("DB set to {}.".format(v))
        elif k == "dbtable":
            kcw.config_set("sql_table", v)
            kcw.verbose_printf("table set to {}".format(v))
        elif k == "username":
            username = v
            kcw.config_set("sql_username", username)
            kcw.verbose_printf("username : {}.".format(username))
        elif k == "password":
            password = v
            kcw.config_set("sql_password", password)
            kcw.verbose_printf("password : {}.".format(password))
        elif k == "sleep":
            kcw.config_set("sleep", float(v))
            kcw.verbose_printf("sleep : {} secs.".format(float(v)))
        elif k == "tag":
            tag = v
            kcw.config_set("tag", tag)
            kcw.verbose_printf("tag : {}.".format(tag))
        elif k == "cachedata":
            cachedata = (v == 'True')
            kcw.config_set("cachedata", cachedata)
            kcw.verbose_printf("Caching status {}.".format(cachedata))
        elif k == "usecache":
            usecache = (v == 'True')
            kcw.config_set("usecache", usecache)
            kcw.verbose_printf("Using caching status {}".format(usecache))
        elif k == "cachedir":
            cachedirectory = os.path.expanduser(v)
            kcw.config_set("cachedirectory", cachedirectory)
            kcw.verbose_printf("Cache directory set to {}".format(cachedirectory))
        elif k == "flag":
            flag = v
            kcw.verbose_printf("flag : {}.".format(flag))
        elif k == "fifo":
            wallpaper_fifo = os.path.expanduser(v)
            kcw.config_set("wallpaper_fifo", wallpaper_fifo)
            kcw.verbose_printf("Wallpaper fifio set to {}.".format(wallpaper_fifo))
        elif k == "ssl":
            ssl = (v == "True")
            kcw.verbose_printf("SSL set to {}".format(ssl))
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

    # print warning.
    if int(sys.version.split()[0].split(".")[2]) < 9 and \
        int(sys.version.split()[0].split(".")[1]) <= 7 and \
        int(sys.version.split()[0].split(".")[0]) <= 2:
        kcw.warning_printf(
            "version 2.7.9 or greater is required for using SSL for urllib2. current %s .\n" % sys.version.split()[0])

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
            kcw.config_set("tag", a)
            kcw.verbose_printf("Search tag override to {}.".format(a))
        elif o in ("-T", "--sleep"):
            kcw.config_set("sleep", float(a))
            kcw.verbose_printf("Sleep time override to {}.".format(float(a)))
        elif o in "cachedir":
            kcw.config_set("cachedirectory", os.path.expanduser(a))
            kcw.verbose_printf("Cache directory override to {}.".format(os.path.expanduser(a)))
        elif o in ("-m", "--sql"):
            kcw.config_set("sql", a)
        elif o in ("--fifo", "-F"):
            kcw.config_set("wallpaper_fifo", a)
            kcw.verbose_printf("FIFO override to {}".format(a))
        elif o in "--ssl":
            kcw.config_set("ssl", a == "True")
        elif o in "--cacheonly":
            kcw.config_set("cacheonly", True)
        elif o == "--clear-cache":
            kcw.verbose_printf("Clearing cache database.\n")
            cachecon = kcw.db.create_sql_cache_connection(kcw.config_get("sql"))
            cachecon.connect(
                kcw.config_get("sql_username"),
                kcw.config_get("sql_password"),
                kcw.config_get("sql_hostname"),
                kcw.config_get("sql_port"),
                kcw.config_get("sql_database"))
            cachecon.clear_cache(kcw.config_get("sql_table"))
            cachecon.disconnect()
            quit(0)
        elif o == "--clear-cache-img":
            kcw.verbose_printf("Clearing image cache.\n")
            cachedirectory = kcw.config_get("cachedirectory")
            lst = os.listdir(cachedirectory)
            for l in lst:
                kcw.verbose_printf("Removing file from cache directory %s.\n" % l)
                fpath = "%s/%s" % (cachedirectory, l)
                os.remove(fpath)
            quit(0)
        elif o == "--random":
            kcw.kc_array_args.append("--random")
        elif o in ("--quality", "-q"):
            if a in kcw.QUALITY_CONSTANT.keys():
                kcw.config_set("quality", kcw.QUALITY_CONSTANT[a])
            else:
                kcw.config_set("quality", int(a))
                kcw.verbose_printf("Quality set to %s" % kcw.config_get("quality"))

        elif o in ("-A", "--advanced_konachan_flag"):
            kcw.kc_array_args.append(a)
        else:
            pass
