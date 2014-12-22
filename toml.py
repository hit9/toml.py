# coding=utf8
#
# Python parser for Toml(https://github.com/mojombo/toml)
# An improved version of \
# toml-ply(https://github.com/marksteve/toml-ply)
# License: MIT
# Author: hit9
#

__version__ = '0.1'  # Current supported Toml's version

import sys
from ply import lex
from ply import yacc
from six import string_types
from datetime import datetime

DATETIME_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

if sys.version_info >= (3, 0):
    PY_VERSION = 3
else:
    PY_VERSION = 2


class TomlSyntaxError(SyntaxError):
    pass


class TomlLexer(object):

    tokens = (
        "BOOLEN",
        "KEY",
        "KEYGROUP",
        "EQUALS",
        "DATETIME",
        "STRING",
        "FLOAT",
        "INTEGER",
    )

    literals = "[],"

    t_ignore = "\x20\x09"  # ignore space(x20) and tab(x09)
    t_ignore_COMMENT = r'\#.*'  # comments
    t_EQUALS = r'='

    def t_BOOLEN(self, t):
        r'true | false'
        t.value = (t.value == "true")
        return t

    def t_KEY(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_#\?]*'
        return t

    def t_KEYGROUP(self, t):
        r'\[([a-zA-Z_][a-zA-Z0-9_#\?]*\.?)+\]'
        t.value = tuple(t.value[1:-1].split('.'))  # cast to group
        return t

    def t_DATETIME(self, t):
        # ISO 8601 dates: 1979-05-27T07:32:00Z
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
        t.value = datetime.strptime(t.value, DATETIME_ISO8601_FORMAT)
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        s = t.value[1:-1]

        c = 0  # index to go through the string
        l = len(s)
        o = ""

        # escaping string
        # \b     - backspace       (U+0008)     [x]
        # \t     - tab             (U+0009)     [x]
        # \n     - linefeed        (U+000A)     [x]
        # \f     - form feed       (U+000C)     [x]
        # \r     - carriage return (U+000D)     [x]
        # \"     - quote           (U+0022)     [x]
        # \/     - slash           (U+002F)     [-]
        # \\     - backslash       (U+005C)     [x]
        # \uXXXX - unicode         (U+XXXX)     [-]

        while c < l:
            if s[c] == "\\":
                c += 1
                if s[c] == "t":
                    o += "\t"
                elif s[c] == "n":
                    o += "\n"
                elif s[c] == '"':
                    o += "\""
                elif s[c] == "r":
                    o += "\r"
                elif s[c] == "\\":
                    o += "\\"
                elif s[c] == "f":
                    o += "\f"
                elif s[c] == "b":
                    o += "\b"
                else:
                    raise TomlSyntaxError(
                        "Unexpected escape character: %s" % s[c]
                    )
            else:
                o += s[c]
            c += 1
        t.value = o
        return t

    def t_FLOAT(self, t):
        r'([-]?(\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'[-]?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise TomlSyntaxError(
            "Illegal character: '%s' at Line %d" % (t.value[0], t.lineno)
        )

    def __init__(self):
        self.lexer = lex.lex(module=self)


class TomlParser(object):

    tokens = TomlLexer.tokens

    def p_error(self, p):
        if p:
            raise TomlSyntaxError(
                "Character '%s' at line %d, \
                token: %r" % (p.value[0], p.lineno, p)
            )
        else:
            raise TomlSyntaxError("SyntaxError at EOF")

    def p_start(self, p):
        # parser start here
        "start : translation_unit"
        p[0] = self.dct

    def p_translation_unit(self, p):
        # unit to find out all assignments
        """
        translation_unit : assignment
                         | translation_unit assignment
                         |
        """
        pass

    def p_assignment_key(self, p):
        # look up all keys
        """
        assignment : KEY EQUALS value
        """
        d = self.dct
        # slide to the current keygroup's depth
        for key in self.keygroup:
            d = d[key]

        # if duplicate, recover the old one
        # But I really dont know how to raise an error here
        # raise statement seems not working here
        d[p[1]] = p[3]

    def p_assignment_keygroup(self, p):
        # look up all keygroups
        """
        assignment : KEYGROUP
                   | assignment KEYGROUP
        """
        self.keygroup = p[len(p) - 1]
        d = self.dct

        for key in self.keygroup:
            # init the keygroup's value to empty dict
            d = d.setdefault(key, {})

    def p_value(self, p):
        # values can be array, int, datetime, float, string integer, boolen
        """
        value : array
              | BOOLEN
              | DATETIME
              | STRING
              | FLOAT
              | INTEGER
        """

        p[0] = p[1]

    def p_array(self, p):
        """array : '[' sequence ']'"""
        p[0] = p[2]

    def p_sequence(self, p):
        # sequence is: a, b, c, d, ..
        """
        sequence : sequence ',' value
                 | sequence ','
                 | value
                 |
        """

        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + [p[3]]

    def __init__(self):
        self.parser = yacc.yacc(module=self, debug=0, write_tables=0)

    def parse(self, toml_str):
        # reset dct and keygroup
        self.dct = dict()  # dict object for parser to return
        self.keygroup = tuple()  # to record current group
        return self.parser.parse(toml_str)


class TomlGenerator(object):  # generate toml string from valid python dict

    g_newline = "\n"

    def g_string(self, v):
        # annoying escaping chars :)
        o = ""
        esc_chars = {
            "\t": "t",
            "\n": "n",
            "\"": '"',
            "\r": "r",
            "\\": "\\",
            "\f": "f",
            "\b": "b",
        }

        for c in v:
            if c in esc_chars:
                o += "\\" + esc_chars[c]
            else:
                o += c

        return '"' + o + '"'

    def g_bool(self, v):
        return "true" if v else "false"

    def g_integer(self, v):
        return str(v)

    def g_float(self, v):
        return str(v)

    def g_datetime(self, v):
        return v.strftime(DATETIME_ISO8601_FORMAT)

    def g_array(self, v):
        lst = [self.gen_value(i) for i in v]
        return "[" + ", ".join(lst) + "]"

    def gen_value(self, v):
        # generate toml format of python data
        if isinstance(v, string_types):
            return self.g_string(v)
        elif isinstance(v, bool):
            return self.g_bool(v)
        elif isinstance(v, int):
            return self.g_integer(v)
        elif isinstance(v, float):
            return self.g_float(v)
        elif isinstance(v, datetime):
            return self.g_datetime(v)
        elif isinstance(v, list):
            return self.g_array(v)
        else:
            raise TomlSyntaxError("Invalid data type: %r" % (type(v), ))

    def gen_section(self, dct, keygroup):
        section, body = [], []

        for key, value in dct.items():
            if isinstance(value, dict):
                section.append(self.gen_section(value, keygroup + [key]))
            else:
                body.append(key + " = " + self.gen_value(value))

        if body and keygroup:
            body.insert(0, "[" + ".".join(keygroup) + "]")

        return self.g_newline.join(body + section)


lexer = TomlLexer()  # build lexer
parser = TomlParser()  # build parser
generator = TomlGenerator()  # init a Generator instance


def loads(toml_str):
    return parser.parse(toml_str)


def dumps(dct):
    return generator.gen_section(dct, [])

if __name__ == '__main__':
    if PY_VERSION == 2:
        input_string = raw_input()
    elif PY_VERSION == 3:
        input_string = input()
    exit(loads(input_string))
