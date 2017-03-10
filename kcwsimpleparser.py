# script that parsing simple config syntax.
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

verbose = False


def kcw_isverobse():
    return verbose

def enable_verbose():
    global verbose
    verbose = True

def verbose_print(formatstr):
    if verbose is True:
        print(formatstr)

# Defined syntax.
SP_COMMENTS_SYNTAX = "#"
SP_EQUAL_SYNTAX = "="


# Trim string from left and right only.
def sp_trim_left_right_trim(line):
    return line.replace(" ", "")


# Return directory table.
def sp_parse_file(cfilename):
    verbose_print("Start parsing file %s" % cfilename)
    try:
        f = open(cfilename, 'r')
        table, err = sp_extract_grammer(f)
        f.close()
        return table, err
    except IOError as err:
        print("Couldn't load config file, %s.\n" % err.message)
        return None, None
    except Exception as err:
        print(err.message)
        quit(1)


# Remove comment from line.
def sp_remove_comment(line):
    com = line.find(SP_COMMENTS_SYNTAX)
    if com == -1:
        return line
    else:
        return line[0:com]


# Extract grammer rule.
def sp_extract_grammer(f):
    # Iterate line per line.
    table = {}
    err = []
    line = 0

    lines = f.read().splitlines()
    for cstringdata in lines:
        statement = sp_remove_comment(cstringdata)
        eq = statement.find("=")

        if eq == -1 and not statement.isspace() and len(statement) > 0:
            err.append("Error on line " + str(line) + ". Not a statement > \"" + cstringdata + "\"")
            return None, err

        if eq == -1:
            line += 1
            continue

        larg = sp_trim_left_right_trim(statement[0:eq - 1])
        rarg = sp_trim_left_right_trim(statement[eq + 1:])

        if rarg.isspace() or len(rarg) == 0:
            err.append("Error on line " + str(line) + ". No right argument > \"" + cstringdata + "\"")
            return None, err

        if larg.isspace() or len(larg) == 0:
            err.append("Error on line " + str(line) + ". No left argument > \"" + cstringdata + "\"")
            return None, err

        table[larg] = rarg
        line += 1

    return table, err
