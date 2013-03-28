toml.py
------

Python parser for [mojombo/toml](https://github.com/mojombo/toml).

Improved version of [marksteve/toml-ply](https://github.com/marksteve/toml-ply)

[![Build Status](https://travis-ci.org/hit9/toml.py.png?branch=dev)](https://travis-ci.org/hit9/toml.py)

Support
-------

Version [V0.1](https://github.com/mojombo/toml/blob/master/versions/toml-v0.1.0.md) of toml.


Install
-------

Codes on branch master are tested.

    pip install git+git://github.com/hit9/toml.py.git@master

Use
----

```python
>>> import toml
>>> toml.loads("""
... [blog]
... [blog.author]
... name = "Tom"
... age = 14
... score = 9.99
... is_child = true
... """)
{'blog': {'author': {'age': 14, 'score': 9.99, 'name': 'Tom', 'is_child': True}}}
```

Unicode string are also supported:

```python
>>> toml.loads(u"""
... name = "汤姆"
... """)
{u'name': u'\u6c64\u59c6'}
```

Empty input:(only spaces, tabs or newlines)

```python
>>> toml.loads(" ")
{}
```

input only `#` comments:

```python
>>> toml.loads("# only comments!")
{}
```

from command line:

```
$ cat some.toml | python -m toml
{'name': 'Tom'}
$ echo "n = 1.3" | python -m toml
{'n': 1.3}

```

Sepcific Notes
--------------

**Each piece of notes bellow comes from [mojombo/toml](https://github.com/mojombo/toml)**, just implemented in toml.py

1. Negative integer and float is ok: `-1` `-0.9`, but positive integer or float in this format is not allowed: `+9` `+8.8`

2. Booleans are always lowercase.

3. Arrays also ignore newlines between the brackets:
```python
>>> import toml
>>> toml.loads("""
... arr = [
...     2,
...     3,
...     4,
... ]
... """)
{'arr': [2, 3, 4]}
```
As you see, terminating commas are ok before the closing bracket.

4. Arrays can be nested
```python
>>> toml.loads("""
... arr = [[1,2,[3,4],5]]
... """)
{'arr': [[1, 2, [3, 4], 5]]}
```
5. You don't need to specify all the superkeys if you don't want to. TOML knows how to do it for you.
```python
>>> toml.loads("""
... [x.y.z]
... a = "somestr"
... """)
{'x': {'y': {'z': {'a': 'somestr'}}}}
```
6. For flaot, there must be at least one number on each side of the decimal point.
```
.5  # bad
```
7. Datetimes are ISO 8601 dates, only full zulu form is allowed.
```
 >>> toml.loads("""date = 1979-05-27T07:32:00Z""")
{'date': datetime.datetime(1979, 5, 27, 7, 32)}
```
8. String escaping, `toml.py` dosen't implement the forward slash and `\uXXXX`
```
\b     - backspace       (U+0008)     [x]
\t     - tab             (U+0009)     [x]
\n     - linefeed        (U+000A)     [x]
\f     - form feed       (U+000C)     [x]
\r     - carriage return (U+000D)     [x]
\"     - quote           (U+0022)     [x]
\/     - slash           (U+002F)     [-]
\\     - backslash       (U+005C)     [x]
\uXXXX - unicode         (U+XXXX)     [-]
```
```python
>>> toml.loads(r"""  # attention to the r here, use raw or unicode or \\\\
... path = "C:\\files\\MyPython\\"
... """)
{'path': 'C:\\files\\MyPython\\'}
```


Tests
-----

    $ nosetests -w tests

TODO
----

1. error handle

2. write tests

3. doc for specific about escaping string

4. to fix:Data types may not be mixed.
