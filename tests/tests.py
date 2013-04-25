# coding=utf8
# run test for toml.py
#

import os
import sys
import yaml
from nose.tools import raises
from functools import wraps

sys.path.append("..")
import toml
from toml import TomlSyntaxError as e


def readf(name):
    if time == 0:
        p = os.path.join("tomls", name + ".toml")
    else:
        p = os.path.join("_tomls", name + ".toml")
    print "Read from: " + p
    return open(p).read()


def t(func):
    # get item's name   test_string => string
    name = func.__name__[5:]

    @wraps(func)
    def _t():
        # read file by filename
        dct = toml.loads(readf(name))
        # write to  _toml/..
        p = os.path.join("_tomls", name + ".toml")
        print "Dump to: " + p
        c = toml.dumps(dct)
        open(p, "w").write(c)
        return func(dct)
    return _t


def u(func):
    # unicode
    name = func.__name__[5:]

    @wraps(func)
    def _u():
        print "Unicode Tests: ",
        dct = toml.loads(readf(name).decode("utf8"))
        p = os.path.join("_tomls", name + ".toml")
        print "Dump to: " + p
        c = toml.dumps(dct)
        open(p, "w").write(c.encode("utf8"))
        return func(dct)
    return _u


###############################
# test parser
###############################


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


@t
def test_boolen(dct):
    assert dct == {"do_u_love_me": False, "see": True}


@t
def test_empty(dct):
    assert dct == {}


@t
def test_datetime(dct):
    from datetime import datetime
    assert dct == dict(
        datetime=datetime(1979, 5, 27, 7, 32)
    )


@t
def test_keygroup(dct):
    assert dct == {
        "a": {
            "name": "Toml",
            "email": "Toml@github.com",
            "age": 78,
            "b": {
                "m": 13.9
            }
        },
        "b": {
            "c": {
                "d": {
                    "e": -0.999
                }
            }
        }
    }


@t
def test_array(dct):
    assert dct == {
        "a": ["你", "是", "谁"],
        "b": [1, 2, 3, ]
    }


@t
def test_empty_keygroup(dct):
    assert dct == {
        "a": {
            "b": {
                "c": {}
            }
        },
        "c": {
            "d": {}
        }
    }


########################################
# official test suite
########################################
@t
def test_hard_example(dct):
    print "Official test suite: hard_example.toml"
    assert dct == yaml.load(open("yaml/hard_example.yaml").read())


@t
def test_example(dct):
    print "Official test suite: example.toml"
    assert dct == yaml.load(open("yaml/example.yaml").read())

time = 0

if __name__ == '__main__':
    import nose
    nose.run(argv=['tests.py', '-v', '-x', '--process-timeout=10', '--nocapture'])
    time += 1
    nose.run(argv=['tests.py', '-v', '-x', '--process-timeout=10', '--nocapture'])
