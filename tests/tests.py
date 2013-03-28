# coding=utf8
# run test for toml.py
#

import os
import sys
# i have to use wraps from functools to make nose works with custom decorators
from nose.tools import raises
from functools import wraps

sys.path.append("..")
import toml
from toml import TomlSyntaxError as e


def readf(name):
    return open(os.path.join("tomls", name + ".toml")).read()


def t(func):
    # get item's name   test_string => string
    name = func.__name__[5:]

    @wraps(func)
    def _t():
        # read file by filename
        dct = toml.loads(readf(name))
        return func(dct)
    return _t


def u(func):
    # unicode
    name = func.__name__[5:]

    @wraps(func)
    def _u():
        dct = toml.loads(readf(name).decode("utf8"))
        return func(dct)
    return _u


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


@t
def test_float(dct):
    assert dct == dict(
        a=1.0,
        b=0.3,
        c=0.5,
        d=8.8,
        e=-9.4,
        f=11.6
    )


@t
def test_integer(dct):
    assert dct == dict(
        a=1,
        b=999,
        c=-888,
        d=05
    )


@raises(e)
@t
def test_bad_float_1():
    pass


@raises(e)
@t
def test_bad_float_2():
    pass


@raises(e)
@t
def test_bad_integer():
    pass


@u
def test_unicode(dct):
    assert dct == {u"name": u"你好!", u"title": u"汤姆"}


@t
def test_chinese(dct):
    assert dct == dict(
        name="小明",
        email="xiaoming@126.com"
    )


if __name__ == '__main__':
    exit("run nosetests")
