# coding=utf8
#
# Python parser for toml (Tom's Obvious, Minimal Language)
# Home: https://github.com/mojombo/toml
# Note: This is an improved version of \
# toml-ply(https://github.com/marksteve/toml-ply)
# License: MIT
#

__version__ = '0.1'

from ply import lex
from ply import yacc
from datetime import datetime


class TomlSyntaxError(SyntaxError):
    pass


# year-month-day-T-hour-minute-timezone
ISO8601 = "%Y-%m-%dT%H:%M:%SZ"

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

literals = ["[", "]", ","]

# ignore space(x20) and tab(x09)
t_ignore = "\x20\x09"

# comments
# key = "value" # Yeah, you can do this.
t_ignore_COMMENT = r'\#.*'


t_EQUALS = r"="


def t_BOOLEN(t):
    r'true|false'
    t.value = (t.value == "true")
    return t


def t_KEY(t):
    r'[a-zA-Z_][a-zA-Z0-9_#\?]*'
    return t


# keygroups can be nested. so use tuple to store this.
# e.g. [a.b.c] => ('a', 'b', 'c')
def t_KEYGROUP(t):
    r'\[([a-zA-Z_][a-zA-Z0-9_#\?]*\.?)+\]'
    t.value = tuple(t.value[1:-1].split('.'))
    return t


# ISO 8601 dates: 1979-05-27T07:32:00Z
def t_DATETIME(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
    t.value = datetime.strptime(t.value, ISO8601)
    return t


# escape string
# \b     - backspace       (U+0008)     [x]
# \t     - tab             (U+0009)     [x]
# \n     - linefeed        (U+000A)     [x]
# \f     - form feed       (U+000C)     [x]
# \r     - carriage return (U+000D)     [x]
# \"     - quote           (U+0022)     [x]
# \/     - slash           (U+002F)     [-]
# \\     - backslash       (U+005C)     [x]
# \uXXXX - unicode         (U+XXXX)     [-]
# But i dont think toml should escape this char: /
# see mojombo/toml/issue#173. I dont want to escape forward slashes
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # remove fisrt double quote and last double quote as value
    s = t.value[1:-1]
    # handle escaping characters
    c = 0
    l = len(s)
    o = ""

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


# Feeling negative? Do what's natural.
# toml means, don't use this: +1.79, use 1.79 instead
def t_FLOAT(t):
    r'([-]?(\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
    t.value = float(t.value)
    return t


# dont use +4,  use 4 instead.
# negative integer is ok: -4
# TODO: to forbid this format: 04
def t_INTEGER(t):
    r'[-]?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise TomlSyntaxError(
        "Illegal character: '%s' at Line %d" % (t.value[0], t.lineno)
    )


# build lexer
lex.lex()

# return dict
dct = None
# temp global var to record keygroup
keygroup = None


def p_error(p):
    if p:
        raise TomlSyntaxError(
            "SyntaxError: character '%s' at line %d , token is: %r" % (p.value[0], p.lineno, p)
        )
    else:
        raise TomlSyntaxError("SyntaxError at EOF")


# start rule, store dct
def p_start(p):
    "start : translation_unit"
    p[0] = dct


# unit to lookup all assignments
def p_translation_unit(p):
    """
    translation_unit : assignment
                     | translation_unit assignment
                     |
    """
    pass


# lookup all keys
def p_assignment_keys(p):
    """assignment : KEY EQUALS value"""
    # TODO: if key already in dct, raise error
    # reference global dct with d
    d = dct
    # if keys are in some keygroup
    for k in keygroup:
        # @marksteve 's way is right!
        d.setdefault(k, {})
        d = d[k]
    d[p[1]] = p[3]


# looup all keygroups
def p_assignment_keygroup(p):
    """assignment : KEYGROUP
                  | assignment KEYGROUP"""
    global keygroup
    keygroup = p[len(p) - 1]


# values can be array, int, datetime, float, string integer, boolen
def p_value(p):
    """value : array
             | BOOLEN
             | DATETIME
             | STRING
             | FLOAT
             | INTEGER"""

    p[0] = p[1]


# Arrays are square brackets with other primitives inside.
# Whitespace is ignored. Elements are separated by commas.
# Data types may not be mixed.
def p_array(p):
    """array : '[' sequence ']'"""
    p[0] = p[2]


# terminating commas are ok before the closing bracket.
def p_sequence(p):
    """sequence : sequence ',' value
                | sequence ','
                | value
                | """

    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]


parser = yacc.yacc(debug=0, write_tables=0)


def loads(s):
    global dct
    global keygroup
    # reset return dict
    dct = dict()
    keygroup = tuple()
    return parser.parse(s)

if __name__ == '__main__':
    exit(loads(raw_input()))
