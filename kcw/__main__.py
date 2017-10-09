# Entry point as executable python script.
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
from distutils.spawn import find_executable

from kcw.kcwallpaper import main
from kcwlog import errorf

# Check if the executable dependencies exists on the system.
utilprogdep = ["swp", "konachan"]
for program in utilprogdep:
    if not find_executable(program, os.environ['PATH'] + ":" + os.getcwd()):
        errorf("Program '{}' does not exist, program will terminate now.", program)
        exit(0)
else:
    if __name__ == '__main__':
        main()
