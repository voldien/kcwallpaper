#!/usr/bin/python2.7
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
import atexit
import signal
import time
import urllib2

import kcw.db
from kcw import *


def main():
    """ Main function.  """

    # Read options.
    kcw.kcwreadoptions.kcw_read_options(DEFAULT_CONFIG_PATH)

    # Software interrupt.
    def catch_signal(sig, frame):
        if sig is signal.SIGINT:
            if sqlcon:
                sqlcon.disconnect()
            if swp:
                swp.kill()
            quit(0)
        if sig is signal.SIGCHLD:
            kcw_errorf("Child process terminated.\n")
            quit(1)
        else:
            kcw_errorf("Unknown signal %d.\n" % sig)

    def kill_child_ps():
        if swp is not None:
            swp.kill()

    # Setup for making the program terminate properly.
    atexit.register(kill_child_ps)
    signal.signal(signal.SIGINT, catch_signal)

    # Create wallpaper process for display pictures.
    kcw_verbose_print("Starting wallpaper process.\n")
    swp_args.append("-p")
    swp_args.append(kcw.kcw_config_get("wallpaper_fifo"))
    if kcw.kcw_get_verbosity() >= KCW_VERBOSE:
        swp_args.append("--verbose")
    swp = kcw.kcw_create_popen(swp_args)
    if not swp:
        quit(1)

    # Create cache directory
    if kcw.kcw_config_get("cachedata") and not os.path.isdir(kcw.kcw_config_get("cachedirectory")):
        kcw_verbose_print("Creating cache directory %s." % kcw.kcw_config_get("cachedirectory"))
        kcw_create_directory(kcw.kcw_config_get("cachedirectory"))

    # Create mysql connection and connect. (Optional)
    if kcw.kcw_config_get("use_sql"):

        try:
            sqlcon = kcw.db.kcw_create_sql(kcw.kcw_config_get("sql"))
            sqlcon.connect(
                kcw.kcw_config_get("sql_username"),
                kcw.kcw_config_get("sql_password"),
                kcw.kcw_config_get("sql_hostname"),
                kcw.kcw_config_get("sql_port"),
                kcw.kcw_config_get("sql_database"))

        except Exception as err:
            # Disable caching if connection fails.
            kcw.kcw_config_set("cachedata", False)
            kcw.kcw_config_set("usecache", False)
            kcw.kcw_config_set("cacheonly", False)
            sqlcon = None

    # Set http protocol.
    http_pro = URL_PROTOCOL_QUALIFIER[kcw.kcw_config_get("ssl")]
    kc_array_args.append(KONACHAN_SECURITY_FLAG[kcw.kcw_config_get("ssl")])

    # Data associate with
    i = 0
    isalive = True
    imgid = 0
    response = None
    imgdata = None
    extrline = None
    kc_cmd = reduce(lambda a, x: a + " " + x, kc_array_args)
    get_kcw_cmd = lambda i: kc_cmd % (kcw.kcw_config_get("tag"), i)

    # Sleep in order allow the swp program to start up properly. Causes it
    # crash otherwise.
    time.sleep(0.2)

    # Main program loop.
    while isalive:

        # Don't query in 'cacheonly' mode.
        if not kcw.kcw_config_get("cacheonly"):

            # Fetch data from konachan program.
            kc_cmdf = get_kcw_cmd(i)
            p = os.popen(kc_cmdf, 'r')

            #
            try:
                output = p.readline()
            except IOError as err:
                kcw_errorf(err.message)

            # Extract values from the query tool.
            if len(output) > 0:
                extrline = output.split()
            elif kcw.kcw_config_get("use_sql") and sqlcon:
                # Restart the query.
                kcw_verbose_print("No result from konachan.\n")
                i = 1
                continue

            # The order which the output data is stdout.
            url = extrline[0]
            sample = extrline[1]
            preview = extrline[2]
            score = extrline[3]
            imgid = extrline[4]
            tags = reduce(lambda a, x: a + " " + x, extrline[5:])

            # Get URL.
            fetchurl = extrline[abs(2 - kcw.kcw_config_get("quality"))]

        # Check if image exists and cache is enabled.
        if (kcw.kcw_config_get("usecache") and sqlcon.check_img_exists(kcw.kcw_config_get("sql_table"), imgid)) \
                or (kcw.kcw_config_get("cacheonly") and kcw.kcw_config_get("usecache")):
            if not kcw.kcw_config_get("cacheonly"):
                cachefilename = sqlcon.get_cached_img_url_by_id(
                                                                        kcw.kcw_config_get("sql_table"), imgid)
            else:
                cachefilename = sqlcon.get_cached_img_url_by_tag(kcw.kcw_config_get("sql_table"),
                                                                    QUALITY_SQL_COLUMN[
                                                                    kcw.kcw_config_get("quality")],
                                                                    kcw.kcw_config_get("tag"), i)

            if not cachefilename:
                i += 1
                continue

            #
            fpath = "{}/{}".format(kcw.kcw_config_get("cachedirectory"), cachefilename)
            kcw_verbose_print("Using cached file %s.\n", fpath)
            try:
                with open(fpath, 'rb') as fcach:
                    imgdata = fcach.read()
                fcach.close()
            except Exception as err:
                kcw_errorf(err.message)
        else:
            if kcw.kcw_config_get("hasInternet"):
                try:
                    # Create URL.
                    url = "{}://www.{}".format(http_pro, fetchurl)
                    kcw_verbose_print("Downloading image from URL : %s\n", fetchurl)
                    # basename for the image file.
                    basename = os.path.basename(url).decode().replace("%20", " ")
                    #   Create connection.
                    response = urllib2.urlopen(url)
                    # Download all data.
                    imgdata = response.read()
                    response.close()
                    del response

                except urllib2.URLError as err:
                    kcw_errorf(err.message)

                # Cache image if caching is enabled and sql connection exists.
                if kcw.kcw_config_get("cachedata") and sqlcon:
                    kcw_verbose_print("Caching downloaded image data to %s as %s.\n",
                                      kcw.kcw_config_get("cachedirectory"), basename)

                    fpath = "%s/%s" % (kcw.kcw_config_get("cachedirectory"), basename)
                    cachef = open(fpath, 'wb')
                    cachef.write(imgdata)
                    cachef.close()

                    # Add image and its attributes to database.
                    kcw_verbose_print("Adding image to SQL database.\n")
                    sqlcon.add_img_entry(kcw.kcw_config_get("sql_table"), basename, preview, score, imgid, tags)
            #
            elif kcw_config_get("usecache"):
                print("No internet connection.\n")
                cachefilename = sqlcon.get_cached_img_url_by_tag(kcw.kcw_config_get("sql_table"),
                                                                         kcw.kcw_config_get("tag"))
                with open(kcw.kcw_config_get("cachedirectory") + cachefilename, 'rb') as fcach:
                    imgdata = fcach.read()
                fcach.close()
            # Wait intill internet has returned
            else:
                print("No internet connection.\n")
                exit(1)

        # Write image data to FIFO.
        kcw.kcw_write_fifo(kcw.kcw_config_get("wallpaper_fifo"), imgdata)

        # Sleep intill next fetch.
        time.sleep(kcw.kcw_config_get("sleep"))
        i += 1

    # Cleanup.
    sqlcon.disconnect()

    return 0

#
if __name__ == '__main__':
    main()
