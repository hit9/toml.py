#coding=utf8
from ply import lex
from ply import yacc
from ply.lex import TOKEN
from datetime import datetime
from re import UNICODE

# escape string
"""
\b     - backspace       (U+0008)
\t     - tab             (U+0009)
\n     - linefeed        (U+000A)
\f     - form feed       (U+000C)
\r     - carriage return (U+000D)
\"     - quote           (U+0022)
\/     - slash           (U+002F)
\\     - backslash       (U+005C)
\uXXXX - unicode         (U+XXXX)
"""

# see mojombo/toml/issue#173. I dont want to escape forward slashes
ES = r"(\\([btnfr\"\\u]|[0-7]{1,3}|x[a-fA-F0-9]+))"

STR = r'\"([^"\\\n]|'+ES+')*\"'


class TomlSyntaxError(SyntaxError):
    pass

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'

tokens = (
    "KEY",
    "KEYGROUP",
    "EQUALS",
    "DATETIME",
    "STRING",
    "FLOAT",
    "INTEGER",
    "BOOLEN"
)

literals = ["[", "]", ","]

# ignore space(x20) and tab(x09)
t_ignore = "\x20\x09"

# comments
t_ignore_COMMENT = r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise TomlSyntaxError(
        u"Illegal character '{0}' at line {1}".format(
            t.value[0], t.lexer.lineno
        )
    )


t_EQUALS = r"="


def t_KEY(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_KEYGROUP(t):
    r'\[([a-zA-Z_][a-zA-Z0-9_]*\.?)+\]'
    t.value = tuple(t.value[1:-1].split('.'))
    return t


# ISO 8601 dates: 1979-05-27T07:32:00Z
def t_DATETIME(t):
    r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
    t.value = datetime.strptime(t.value, ISO8601)
    return t


@TOKEN(STR)
def t_STRING(t):
    t.value = t.value[1:-1]
    return t


def t_FLOAT(t):
    r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
    t.value = int(t.value)
    return t


def t_BOOLEN(t):
    r'true|false'
    t.value = t.value == "true"
    return t

# build lexer
lex.lex(reflags=UNICODE)

#return dict
dct = None


def p_error(p):
    raise TomlSyntaxError(
        "SyntaxError at '%r'" % (p, )
    )

# start rule, store dct
def p_start(p):
    "start : translation_unit"
    p[0] = dct


# unit to lookup all assignments
def p_translation_unit(p):
    """
    translation_unit : assignment
                     | translation_unit assignment
    """
    pass


def p_assignment(p):
    """assignment : KEY EQUALS value"""
    dct[p[1]] = p[3]


def p_value(p):
    """value : DATETIME
             | STRING
             | FLOAT
             | INTEGER
             | BOOLEN"""

    p[0] = p[1]


parser = yacc.yacc(debug=1, write_tables=0)


def loads(s):
    global dct
    # reset return dict
    dct = dict()
    return parser.parse(s)
