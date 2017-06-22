# konachan wallpaper configuration.
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
import kcw.kcwlog
config = {}


# Set configuration.
def kcw_config_set(key, v):
    kcw.kcwlog.kcw_debug_printf("Set ({},{})".format(key,v))
    config[key] = v


# Get configuration by key.
def kcw_config_get(key):
    return config[key]
