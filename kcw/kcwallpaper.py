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
import shutil
import signal
import time

import kcw.db
import kcwreadoptions
from kcw import get_version
from kcw.kcwconfiguration import config_get, config_set
from kcw.kcwlog import *
from kcw.kcwmisc import *
from kcwdefault import *

if sys.version_info[0] == 2:
    import urllib2 as urllib3
else:
    import urllib3


def main():
    """
    Main function.
    """

    swp = None
    sqlcon = None

    # Check if the default configuration file exists.
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        # Default file does not exist.
        shutil.copy("{}/{}".format(get_share_directory_path(), CONFIG_FIELNAME), DEFAULT_CONFIG_PATH)

    # Read options.
    kcwreadoptions.read_options(DEFAULT_CONFIG_PATH)

    # Software interrupt.
    def catch_signal(sig, frame):
        if sig is signal.SIGINT:
            if sqlcon:
                sqlcon.disconnect()
            if swp:
                swp.kill()
            os.remove(config_get("wallpaper_fifo"))
            quit(0)
        if sig is signal.SIGCHLD:
            errorf("Child process terminated.\n")
            quit(1)
        else:
            errorf("Unknown signal %d.\n" % sig)

    def kill_child_ps():
        if swp is not None:
            swp.kill()

    # Prevent urllib from I/O blocking forever.
    socket.setdefaulttimeout(5)

    # Setup for making the program terminate properly.
    atexit.register(kill_child_ps)
    signal.signal(signal.SIGINT, catch_signal)

    # Create wallpaper process for display pictures.
    verbose_printf("Starting wallpaper process.\n")

    # Simple wallpaper command line.

    swp_args = list(["swp", "--fullscreen", "-C"])
    swp_args.append("--title=konachan wallpaper - {}".format(get_version()))
    swp_args.append("-p")
    swp_args.append(config_get("wallpaper_fifo"))
    # Display wallpaper verbose only in debug mode.
    if get_verbosity() >= KCW_DEBUG:
        swp_args.append("--verbose")

    try:
        swp = create_popen(swp_args)
    except Exception as err:
        errorf("Failed to create swp process for displaying the image.\n\t {}.\n", err)
        quit(1)

    # Create cache directory
    if config_get("cachedata") and not os.path.isdir(config_get("cachedirectory")):
        verbose_printf("Creating cache directory %s." % config_get("cachedirectory"))
        create_cache_directory(config_get("cachedirectory"))

    # Create mysql connection and connect. (Optional)
    if config_get("use_sql") and (config_get("usecache") or config_get("cachedata")):

        try:
            sqlcon = kcw.db.create_sql_cache_connection(config_get("sql"))
            sqlcon.connect(
                config_get("sql_username"),
                config_get("sql_password"),
                config_get("sql_hostname"),
                config_get("sql_port"),
                config_get("sql_database"))

        except Exception as err:
            # Disable caching if connection fails.
            errorf("Failed creating SQL cache connection - Reversing back to streaming.\n\t {}.\n", err.message)
            config_set("cachedata", False)
            config_set("usecache", False)
            config_set("cacheonly", False)
            sqlcon = None

    # Check if there exist cache in respect to current setting.
    if config_get("cacheonly"):
        if sqlcon.num_cache_entries(config_get("sql_table"), config_get("tag"), config_get("quality")) == 0:
            errorf("No cached data available for tag '{}' with quality : {}.\n", config_get("tag"),
                   QUALITY_SQL_COLUMN[config_get("quality")])
            exit(1)

    # Set http protocol.
    http_pro = URL_PROTOCOL_QUALIFIER[config_get("ssl")]
    kc_array_args.append(KONACHAN_SECURITY_FLAG[config_get("ssl")])

    # Data associate with
    i = 0
    isalive = True
    imgid = 0
    imgdata = None
    extrline = None
    kc_cmd = str(" ").join(kc_array_args)

    def compute_kc_cmd(j):
        return kc_cmd % (config_get("tag"), j)
    get_kcw_cmd = compute_kc_cmd

    # Sleep in order allow the swp program to start up properly.
    # It cause the program to crash otherwise.
    time.sleep(0.2)

    # Main verbose.
    verbose_printf("Starting main wallpaper loop with tag set as '{}'", config_get("tag"))

    # Main program loop.
    while isalive:
        verbose_printf("\n-----------------------------------\n")
        verbose_printf("Starting loading image with index {}.\n", i)

        # Don't query in 'cacheonly' mode.
        if not config_get("cacheonly") and config_get("hasInternet"):

            # Fetch data from konachan program.
            kc_cmdf = get_kcw_cmd(i)
            try:
                pkonachan = subprocess.Popen(kc_cmdf, shell=True,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, err = pkonachan.communicate()
                if pkonachan.returncode != 0:
                    config_set("hasInternet", False)
            except IOError as err:
                verbose_printf("No Internet detected - Disabling stream.")
                debug_printf("Failed read from konachan program : %s", err.message)
                config_set("hasInternet", False)
                continue

            # Extract values from the query tool.
            if len(output) > 0:
                extrline = output.split()
            elif config_get("use_sql") and sqlcon:
                # Restart the query.
                verbose_printf("No result from konachan.\n")
                i = 1
                continue

            # The order which the output data is stdout.
            score = extrline[3]
            imgid = extrline[4]
            tags = " ".join(extrline[5:])

            # Get URL.
            fetchurl = extrline[abs(2 - config_get("quality"))]

        # Check if image exists and cache is enabled.
        if (config_get("usecache") and sqlcon.check_img_exists(config_get("sql_table"), imgid)) \
                or (config_get("cacheonly") and config_get("usecache")):

            # Check image exist by konachan image ID.
            if not config_get("cacheonly"):
                cachefilename = sqlcon.get_cached_img_url_by_id(
                    config_get("sql_table"), imgid)
            else:
                cachefilename = sqlcon.get_cached_img_url_by_tag(config_get("sql_table"),
                                                                 config_get("quality"),
                                                                 config_get("tag"), i)
            # Check if failed fetch path.
            if not cachefilename:
                i = 0
                continue

            # Create cache image path.
            fpath = "{}/{}".format(config_get("cachedirectory"), cachefilename).encode()

            # Load image.
            verbose_printf("Using cached file {}.\n", fpath)
            try:
                with open(fpath, 'rb') as fcach:
                    imgdata = fcach.read()
            except IOError as err:
                errorf(err.message)
            except Exception as err:
                errorf(err.message)

        else:
            if config_get("hasInternet"):
                try:
                    # Create URL string.
                    url = "{}://www.{}".format(http_pro, fetchurl)
                    # basename for the image file.
                    basename = os.path.basename(url).decode().replace("%20", " ")
                    # Create connection.
                    response = urllib3.urlopen(url)
                    # Download all data.
                    verbose_printf("Downloading image from URL : {}\n", fetchurl)
                    imgdata = response.read()
                    # Release connection.
                    response.close()
                    del response

                except Exception as err:
                    errorf(err.message)
                    continue

                # Cache image if caching is enabled and sql connection exists.
                if config_get("cachedata") and sqlcon:
                    # Create image cache file path.
                    fpath = "%s/%s" % (config_get("cachedirectory"), basename)

                    # Save cached image to file.
                    try:
                        with open(fpath, 'wb') as f:
                            f.write(imgdata)
                    except IOError as ioex:
                        errorf("Failed to cache downloaded image to {}.\n\t{}.\n", fpath, ioex.message)
                    #
                    verbose_printf("Cached the downloaded image file to {}.\n",
                                   fpath)

                    # Add image and its attributes to database.
                    verbose_printf("Adding image to SQL database.\n")
                    sqlcon.add_img_entry(config_get("sql_table"), basename, config_get("quality"), score, imgid, tags)
            #
            elif config_get("usecache"):

                #
                errorf("No internet connection.\n")
                cachefilename = sqlcon.get_cached_img_url_by_tag(config_get("sql_table"),
                                                                 config_get("quality"),
                                                                 config_get("tag"), i)
                #
                fpath = "{}/{}".format(config_get("cachedirectory"), cachefilename)
                try:
                    with open(fpath, 'rb') as fcach:
                        imgdata = fcach.read()
                except IOError as err:
                    pass

            # Wait in till internet has returned
            else:
                errorf("No connection to server and cached disabled.\n")
                errorf("Program will wait in till connection comes up again.\n")
                while connection_wait():
                    time.sleep(2.0)
                config_set("hasInternet", True)

        # Write image data to FIFO.
        write_fifo(config_get("wallpaper_fifo"), imgdata)

        # Sleep in till next fetch.
        time.sleep(config_get("sleep"))
        i += 1

    # Cleanup.
    sqlcon.disconnect()

    return 0
