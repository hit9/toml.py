from ply import lex
from ply import yacc

class TomlSyntaxError(SyntaxError):pass

tokens = (
    "KEY",
    "KEYGROUP",
    "EQUALS",
    "STRING",
    "FLOAT",
    "INTEGER",
    "BOOLEN",
    "DATETIME",
    "ARRAY",
    "HASH",
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
    raise TomlSyntaxError(repr(t))

t_EQUALS = r"="

t_KEY = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_KEYGROUP(t):
    r'\[([a-zA-Z_][a-zA-Z0-9_]*\.?)+\]'
    t.value = tuple(t.value[1:-1].split('.'))
    return t

def t_STRING(t):
    #TODO: escape stuff
    r'\"([^\"]|\\.)*\"'
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


lex.lex()
text = open("test.toml").read().decode("utf8")
lex.input(text)
while 1:
    tok = lex.token()
    if not tok: break
    print tok
