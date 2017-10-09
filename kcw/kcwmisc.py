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
import sys
import socket
import subprocess

from kcwlog import verbose_printf, errorf

# FQDN for checking internet connection.
REMOTE_SERVER = "google.com"


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
    except:
        errorf("Unexpected error:", sys.exc_info()[0])
        exit(1)

    return nbytes


def connection_wait():
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
