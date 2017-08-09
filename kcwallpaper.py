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
    kcw.kcwreadoptions.read_options(DEFAULT_CONFIG_PATH)

    # Software interrupt.
    def catch_signal(sig, frame):
        if sig is signal.SIGINT:
            if sqlcon:
                sqlcon.disconnect()
            if swp:
                swp.kill()
            quit(0)
        if sig is signal.SIGCHLD:
            errorf("Child process terminated.\n")
            quit(1)
        else:
            errorf("Unknown signal %d.\n" % sig)

    def kill_child_ps():
        if swp is not None:
            swp.kill()

    # Setup for making the program terminate properly.
    atexit.register(kill_child_ps)
    signal.signal(signal.SIGINT, catch_signal)

    # Create wallpaper process for display pictures.
    verbose_printf("Starting wallpaper process.\n")
    swp_args.append("-p")
    swp_args.append(kcw.config_get("wallpaper_fifo"))
    # Display wallpaper verbose only in debug mode.
    if kcw.get_verbosity() >= KCW_DEBUG:
        swp_args.append("--verbose")

    try:
        swp = kcw.create_popen(swp_args)
    except Exception as err:
        errorf("Failed to create swp process for displaying the image.\n\t {}.\n", err)
        quit(1)

    # Create cache directory
    if kcw.config_get("cachedata") and not os.path.isdir(kcw.config_get("cachedirectory")):
        verbose_printf("Creating cache directory %s." % kcw.config_get("cachedirectory"))
        create_cache_directory(kcw.config_get("cachedirectory"))

    # Create mysql connection and connect. (Optional)
    if kcw.config_get("use_sql"):

        try:
            sqlcon = kcw.db.create_sql(kcw.config_get("sql"))
            sqlcon.connect(
                kcw.config_get("sql_username"),
                kcw.config_get("sql_password"),
                kcw.config_get("sql_hostname"),
                kcw.config_get("sql_port"),
                kcw.config_get("sql_database"))

        except Exception as err:
            # Disable caching if connection fails.
            kcw.errorf("Caching failed, {}.\n", err.message)
            kcw.config_set("cachedata", False)
            kcw.config_set("usecache", False)
            kcw.config_set("cacheonly", False)
            sqlcon = None

    # Set http protocol.
    http_pro = URL_PROTOCOL_QUALIFIER[kcw.config_get("ssl")]
    kc_array_args.append(KONACHAN_SECURITY_FLAG[kcw.config_get("ssl")])

    # Data associate with
    i = 0
    isalive = True
    imgid = 0
    imgdata = None
    extrline = None
    kc_cmd = reduce(lambda a, x: a + " " + x, kc_array_args)

    def compute_kc_cmd(j):
        return kc_cmd % (kcw.config_get("tag"), j)
    get_kcw_cmd = compute_kc_cmd

    # Sleep in order allow the swp program to start up properly.
    # It cause the program to crash otherwise.
    time.sleep(0.2)

    # Main verbose.
    verbose_printf("Starting main wallpaper loop with tag set as '{}'", kcw.config_get("tag"))

    # Main program loop.
    while isalive:
        verbose_printf("\n-----------------------------------\n")
        verbose_printf("Starting loading image with index {}.\n", i)

        # Don't query in 'cacheonly' mode.
        if not kcw.config_get("cacheonly") and kcw.config_get("hasInternet"):

            # Fetch data from konachan program.
            kc_cmdf = get_kcw_cmd(i)
            p = os.popen(kc_cmdf, 'r')

            # Read output data.
            try:
                output = p.readline()
            except IOError as err:
                kcw_errorf(err.message)
                kcw.config_set("hasInternet", False)
                continue

            # Extract values from the query tool.
            if len(output) > 0:
                extrline = output.split()
            elif kcw.config_get("use_sql") and sqlcon:
                # Restart the query.
                verbose_printf("No result from konachan.\n")
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
            fetchurl = extrline[abs(2 - kcw.config_get("quality"))]

        # Check if image exists and cache is enabled.
        if (kcw.config_get("usecache") and sqlcon.check_img_exists(kcw.config_get("sql_table"), imgid)) \
                or (kcw.config_get("cacheonly") and kcw.config_get("usecache")):
            if not kcw.config_get("cacheonly"):
                cachefilename = sqlcon.get_cached_img_url_by_id(
                                                                        kcw.config_get("sql_table"), imgid)
            else:
                cachefilename = sqlcon.get_cached_img_url_by_tag(kcw.config_get("sql_table"),
                                                                 QUALITY_SQL_COLUMN[
                                                                kcw.config_get("quality")],
                                                                 kcw.config_get("tag"), i)
            # Check if failed fetch path.
            if not cachefilename:
                i = 0
                continue

            # Create cache image path.
            fpath = "{}/{}".format(kcw.config_get("cachedirectory"), cachefilename).encode()

            # Load image.
            verbose_printf("Using cached file {}.\n", fpath)
            try:
                with open(fpath, 'rb') as fcach:
                    imgdata = fcach.read()
                fcach.close()
            except IOError as err:
                errorf(err.message)
            except Exception as err:
                errorf(err.message)

        else:
            if kcw.config_get("hasInternet"):
                try:
                    # Create URL string.
                    url = "{}://www.{}".format(http_pro, fetchurl)
                    # basename for the image file.
                    basename = os.path.basename(url).decode().replace("%20", " ")
                    # Create connection.
                    response = urllib2.urlopen(url)
                    # Download all data.
                    verbose_printf("Downloading image from URL : {}\n", fetchurl)
                    imgdata = response.read()
                    # Release connection.
                    response.close()
                    del response

                except urllib2.URLError as err:
                    errorf(err.message)
                    continue

                # Cache image if caching is enabled and sql connection exists.
                if kcw.config_get("cachedata") and sqlcon:
                    # Create image cache file path.
                    fpath = "%s/%s" % (kcw.config_get("cachedirectory"), basename)

                    # Save cached image to file.
                    try:
                        cachef = open(fpath, 'wb')
                        cachef.write(imgdata)
                        cachef.close()
                    except IOError as ioex:
                        errorf("Failed to cache downloaded image to {}.\n\t{}.\n", fpath, ioex.message)
                    #
                    verbose_printf("Cached the downloaded image file to {}.\n",
                                   fpath)

                    # Add image and its attributes to database.
                    verbose_printf("Adding image to SQL database.\n")
                    sqlcon.add_img_entry(kcw.config_get("sql_table"), basename, preview, score, imgid, tags)
            #
            elif config_get("usecache"):

                #
                kcw.errorf("No internet connection.\n")
                cachefilename = sqlcon.get_cached_img_url_by_tag(kcw.config_get("sql_table"),
                                                                 kcw.config_get("tag"))
                #
                fpath = "{}/{}".format(kcw.config_get("cachedirectory"), cachefilename)
                try:
                    with open(fpath, 'rb') as fcach:
                        imgdata = fcach.read()
                    fcach.close()
                except IOError as err:
                    pass

            # Wait in till internet has returned
            else:
                print("No internet connection.\n")
                exit(1)

        # Write image data to FIFO.
        kcw.write_fifo(kcw.config_get("wallpaper_fifo"), imgdata)

        # Sleep in till next fetch.
        time.sleep(kcw.config_get("sleep"))
        i += 1

    # Cleanup.
    sqlcon.disconnect()

    return 0

if __name__ == '__main__':
    main()
