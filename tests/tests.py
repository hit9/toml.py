#
# run test for toml.py
#

import os
import sys
# i have to use wraps from functools to make nose works with custom decorators
from functools import wraps

sys.path.append("..")

import toml


def t(func, unic=False):  # unic - if unicode input
    # get item's name   test_string => string
    name = func.__name__[5:]
    # open file and read
    s = open(os.path.join("tomls", name + ".toml")).read()

    if unic:
        # yes we use utf8 everywhere
        s = s.decode("utf8")

    # this is the parsed toml
    dct = toml.loads(s)

    @wraps(func)
    def _t():
        return func(dct)
    return _t


@t
def test_comment(dct):
    assert dct == {}


@t
def test_key_value(dct):
    assert dct == {"name": "Tom", "age": 10}


@t
def test_ignore_tab_space(dct):
    assert dct == {"name": "mark", "email": "mark@github.com", "score": 9.8}


@t
def test_string(dct):
    assert dct == dict(
        a="Yes,  I am a string",
        b="\b",
        c="\t",
        d="\n",
        e="\f",
        f="\r",
        g="\"",
        h="\\"
    )
