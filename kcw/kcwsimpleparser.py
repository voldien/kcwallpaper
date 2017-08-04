# Script that parse simple config syntax.
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

# Defined grammar syntax.
SP_COMMENTS_SYNTAX = "#"
SP_ASSIGN_SYNTAX = "="


def sp_trim_left_right_trim(line):
    """
    Trim string from left and right only.
    :param line:
    :return:
    """
    return line.replace(" ", "")


def sp_parse_file(path):
    """
    Parse simple configuration file.
    :param path: file path.
    :return: directory table and error array.
    """

    # Check if parameter is valid.
    if not path:
        raise ValueError("file path requires to be a none null parameter.")

    # Load file and extract configuration syntax.
    try:
        f = open(path, 'r')
        table, err = sp_extract_grammar(f)
        f.close()
        return table, err
    except IOError as err:
        print("Couldn't load config file, %s.\n" % err.message)
    except Exception as err:
        print(err.message)
    return None, None


def sp_remove_comment(line):
    """
    Remove comment from line.
    :param line: line statement.
    :return: string without comment.
    """
    com = line.find(SP_COMMENTS_SYNTAX)
    if com == -1:
        return line
    else:
        return line[0:com]


def sp_extract_grammar(f):
    """
    Extract grammar rule.
    :param f: readable file.
    :return: dictionary of each attribute and value.
    """
    table = {}
    err = []
    linecur = 0

    # Extract all lines.
    lines = f.read().splitlines()

    # Iterate line per line.
    for line in lines:
        statement = sp_remove_comment(line)
        eq = statement.find(SP_ASSIGN_SYNTAX)

        # Check if statment exist and if it follows the grammar.
        if eq == -1 and not statement.isspace() and len(statement) > 0:
            err.append("Error on line %s. Not a statement > \"%s\"" % (str(linecur), line))
            return None, err

        if eq == -1:
            linecur += 1
            continue

        # Extract attribute and value of the statement.
        larg = sp_trim_left_right_trim(statement[0:eq - 1])
        rarg = sp_trim_left_right_trim(statement[eq + 1:])

        # Check if value of the attribute is valid.
        if rarg.isspace() or len(rarg) == 0:
            err.append("Error on line %s. No right argument > \"%s\"" % (str(linecur), line))
            return None, err

        # Check if attribute is valid.
        if larg.isspace() or len(larg) == 0:
            err.append("Error on line %s. No left argument > \"%s\"" % (str(linecur), line))
            return None, err

        # Add value with key to dictionary.
        table[larg] = rarg
        linecur += 1

    return table, err
