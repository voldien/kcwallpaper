#!/usr/bin/python
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
from kcwsimpleparser import *
from kcwsql import *
import sys
import getopt
import time
import signal
import os
import urllib2
import subprocess
import atexit

# Global constant variable.
VERSION = "0.9.0"
CONFIG_FIELPATH = "/etc/"
CONFIG_FIELNAME = "kcw.conf"
DEFAULT_USECACHE = True
DEFAULT_CACHEDATA = True
DEFAULT_CACHEFILEDIRECTORY = os.path.expanduser("~/.kcw/cache/")
DEFAULT_SLEEPTIME = 10.0
DEFAULT_SEARCHTAG = "cat"
DEFAULT_USE_MYSQL = True
DEFAULT_MYSQL_PORT = 3389
DEFAULT_MYSQL_HOSTNAME = "localhost"
DEFAULT_MYSQL_USERNAME = "readimg"
DEFAULT_MYSQL_PASSWORD = "randompass"
DEFAULT_MYSQL_DATABASE = "konachan"

#
ssl = True
hasInternet = True
wallpaper_fifo = os.path.expanduser("~/.kcw/wallfifo0")
config_file = CONFIG_FIELPATH + CONFIG_FIELNAME
usecache = DEFAULT_USECACHE
cachedata = DEFAULT_CACHEDATA
cachedirectory = DEFAULT_CACHEFILEDIRECTORY
use_mysql = DEFAULT_USE_MYSQL
mysql_database = 'konachan'
mysql_hostname = DEFAULT_MYSQL_HOSTNAME
mysql_username = DEFAULT_MYSQL_USERNAME
mysql_password = DEFAULT_MYSQL_PASSWORD
mysql_port = DEFAULT_MYSQL_PORT
mysql_table = "img"
tag = DEFAULT_SEARCHTAG
sleep = DEFAULT_SLEEPTIME
sqlcon = None
i = 1
shortopt = "vVmdt:T:h:P:p:c:F:s:"
longoptions = ["version", "verbose", "tag=", "sleep=", "mysql", "config=", "cachedir=", "fifo=", "clear-cache",
               "clear-cache-img", "ssl"]
isAlive = True
swp = None

# Read user input
try:
    opts, args = getopt.getopt(sys.argv[1:], shortopt, longoptions)
except getopt.GetoptError as err:
    print(err.message)

for o, a in opts:
    if o in ("-v", "--version"):
        print("version %s" % VERSION)
        exit(0)
    elif o in ("-V", "--verbose"):
        enable_verbose()
        verbose_print("Enabled verbose.\n")

# print warning.
if int(sys.version.split()[0].split(".")[2]) < 9:
    print("version 2.7.9 or greater is required for using SSL for urllib2. current %s .\n" % sys.version.split()[0])


# Software interrupt.
def catch_signal(sig, frame):
    if sig is signal.SIGINT:
        if sqlcon:
            sqlcon.disconnect()
        if swp:
            swp.kill()
        quit(0)
    if sig is signal.SIGCHLD:
        print("Child process terminated.\n")
        quit(1)
    else:
        print("Unknown signal %d.\n" % sig)


def kill_child_ps():
    if swp is not None:
        swp.kill()

# Setup for making the program terminate properly.
atexit.register(kill_child_ps)
signal.signal(signal.SIGINT, catch_signal)

# Read config file.
config_table, err = sp_parse_file(config_file)
if config_table is None or err:
    if err:
        for k in err:
            print(k)
    else:
        print("config_table is None.\n")
    exit(1)


# Iterate through all of the attributes
for k, v in config_table.iteritems():
    if k in "mysql":
        use_mysql = (v == 'True')
        verbose_print("Using mysql.")
    elif k in "hostname":
        hostname = v
        verbose_print("hostname : {}.".format(hostname))
    elif k in "port":
        port = v
        verbose_print("port : {}.".format(port))
    elif k in "db":
        mysql_database = v
        verbose_print("DB set to {}.".format(mysql_database))
    elif k in "dbtable":
        mysql_table = v
        verbose_print("table set to {}".format(mysql_table))
    elif k in "username":
        username = v
        verbose_print("username : {}.".format(username))
    elif k in "password":
        password = v
        verbose_print("password : {}.".format(password))
    elif k in "sleep":
        sleep = float(v)
        verbose_print("sleep : {} secs.".format(sleep))
    elif k in "tag":
        tag = v
        verbose_print("tag : {}.".format(tag))
    elif k in "cachedata":
        cachedata = (v == 'True')
        verbose_print("Caching status {}.".format(cachedata))
    elif k in "usecache":
        usecache = (v == 'True')
        verbose_print("Using caching status {}".format(usecache))
    elif k in "cachedir":
        cachedirectory = os.path.expanduser(v)
        verbose_print("Cache directory set to {}".format(cachedirectory))
    elif k is "flag":
        flag = v
        verbose_print("flag : {}.".format(flag))
    elif k in "fifo":
        wallpaper_fifo = os.path.expanduser(v)
        verbose_print("Wallpaper fifio set to {}.".format(wallpaper_fifo))
    elif k in "ssl":
        ssl = (v == "True")
        verbose_print("SSL set to {}".format(ssl))
    else:
        print ("%s is not a known configuration attribute.\n" % k)


#   Delete config table because it has served its purpose.
del config_table
del err

# Read user input
try:
    opts, args = getopt.getopt(sys.argv[1:], shortopt, longoptions)
except getopt.GetoptError as err:
    print(err.msg)

for o, a in opts:
    if o in ("-t", "--tag"):
        tag = a
        verbose_print("Search tag overrided to {}.".format(tag))
    elif o in ("-T", "--sleep"):
        print(a)
        sleep = float(a)
        verbose_print("Sleep time overrided to {}.".format(sleep))
    elif o in ("-p", "--pid"):
        pid = int(a)
    elif o in ("-c", "--config"):
        config_file = a
        verbose_print("config file overrided to {}.".format(config_file))
    elif o in "cachedir":
        cachedirectory = os.path.expanduser(a)
        verbose_print("Cache directory overrided to {}.".format(cachedirectory))
    elif o in ("-m", "--mysql"):
        use_mysql = True
        verbose_print("Enable mysql.\n")
    elif o in ("--fifo", "-F"):
        wallpaper_fifo = a
        verbose_print("FIFO overrided to {}".format(wallpaper_fifo))
    elif o in "--ssl":
        ssl = (a == "True")
    elif o == "--clear-cache":
        verbose_print("Clearing cache database.\n")
        tmpsqlcon = sql_connect(mysql_username, mysql_password, mysql_hostname, mysql_port, mysql_database, mysql_table)
        sql_clear_cache(tmpsqlcon, mysql_table)
        tmpsqlcon.close()
        quit(0)
    elif o == "--clear-cache-img":
        verbose_print("Clearing image cache.\n")
        lst = os.listdir(cachedirectory)
        for l in lst:
            verbose_print("Removing file from cache directory %s.\n" % l)
            os.remove(cachedirectory + "/" + l)
        quit(0)

# Create wallpaper process for display pictures.
try:
    verbose_print("Starting wallpaper process.\n")
    args = ["swp", "-p", wallpaper_fifo, "--fullscreen", "-C"]
    if kcw_isverobse():
        args.append("--verbose")
    swp = subprocess.Popen(args)
except Exception as err:
    print("Failed to create swp process for displaying the image. %s." % err)
    quit(1)

# Create cache directory
if cachedata and not os.path.isdir(cachedirectory):
    verbose_print("Creating cache directory %s." % cachedirectory)
    try:
        os.makedirs(cachedata)
    except OSError as err:
        print(err.message)
        exit(1)
    except Exception as err:
        exit(1)

# Create mysql connection and connect. (Optional)
if use_mysql:
    sqlcon = sql_connect(mysql_username, mysql_password, mysql_hostname, mysql_port, mysql_database, mysql_table)
    # Disable caching if connection fails.
    if sqlcon is None:
        cachedata = False
        usecache = False
        sqlcon = None

if ssl:
    konachan_sec_arg = 's'
    http_pro = "https"
else:
    konachan_sec_arg = 'n'
    http_pro = "http"


# Data associate with
response = None
imgdata = None
extrline = ""
while isAlive:

    # Fetch data from konachan program.
    kc_com = "konachan -S%c -t \"%s\" -p %d  -f 'url preview score id'" % (konachan_sec_arg, tag, i)
    p = os.popen(kc_com, 'r')
    try:
        output = p.readline()
    except IOError as err:
        print(err.message)

    # Extract values from the query tool.
    if len(output) > 0:
        extrline = output.split()
    elif use_mysql and sqlcon:
        # Restart the query.
        verbose_print("No result from konachan.\n")
        i = 1
        continue

    # TODO improve once the konachan issue with
    # the order which the output data is stdout.
    url = extrline[0]
    preview = extrline[1]
    score = extrline[2]
    imgid = extrline[3]
    tags = extrline[4]

    # Check if image exists and cache is enabled.
    if usecache and sql_check_img_exists(sqlcon, mysql_table, imgid):
        cachefilename = get_sql_cached_img_url_by_id(sqlcon, mysql_table, imgid)
        verbose_print("Using cached file %s.\n" % cachefilename)
        fpath = "%s/%s" % (cachedirectory, cachefilename)
        with open(fpath, 'rb') as fcach:
            imgdata = fcach.read()
        fcach.close()
    else:
        if hasInternet:
            try:
                # Create URL.
                url = "%s://www.%s" % (http_pro, url)
                verbose_print("Downloading image from URL : %s\n" % url)
                # basename for the image file.
                basename = os.path.basename(url).decode().replace("%20", " ")
                #   Create connection.
                response = urllib2.urlopen(url)
                # Download all data.
                imgdata = response.read()
                response.close()
                del response

            except urllib2.URLError as err:
                print(err.message)

            # Cache image if caching is enabled and sql connection exists.
            if cachedata and sqlcon:
                verbose_print("Caching downloaded image data to %s as %s.\n" % (cachedirectory, basename))
                cachef = open(cachedirectory + basename, 'wb')
                cachef.write(imgdata)
                cachef.close()
                # Add image and its attributes to database.
                verbose_print("Adding image to mysql database.\n")
                add_img_entry(sqlcon, mysql_table, basename, preview, score, imgid, tags)

        elif usecache:
            print("No internet connection.\n")
            cachefilename = get_sql_cached_img_url_by_tag(sqlcon, mysql_table, tag)
            with open(cachedirectory + cachefilename, 'rb') as fcach:
                imgdata = fcach.read()
            fcach.close()
        # Wait intill internet has returned
        else:
            print("No internet connection.\n")

    # Write image data to FIFO.
    try:
        if os.path.exists(wallpaper_fifo):
            f = open(wallpaper_fifo, 'wb')
            f.write(imgdata)
            f.close()
        else:
            print("FIFO file didn't exist.\n")
            exit(1)
    except IOError as err:
        print("Couldn't open fifo file '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except AttributeError as err:
        print("att '%s, %s'.\n", (wallpaper_fifo, err.message))
        exit(1)
    except Exception as err:
        print ("Unexpected error:", sys.exc_info()[0])
        exit(1)

    # delete the data. 
    del output
    del imgdata

    # Sleep intill next fetch.
    time.sleep(sleep)
    i += 1

# Cleanup.
if sqlcon:
    sqlcon.close()
