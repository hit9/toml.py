toml.py
------

Python parser for [mojombo/toml](https://github.com/mojombo/toml).

Improved version of [marksteve/toml-ply](https://github.com/marksteve/toml-ply)

[![Build Status](https://travis-ci.org/hit9/toml.py.png?branch=master)](https://travis-ci.org/hit9/toml.py)

Support
-------

Version [V0.1](https://github.com/mojombo/toml/blob/master/versions/toml-v0.1.0.md) of toml.

**Python>=2.5 or >=3.3**

Install
-------

    pip install toml.py

Parser
------

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
$ echo "n = 1.3" | python -m toml
{'n': 1.3}

```

Generator
---------

```python
>>> import toml
>>> print toml.dumps({'blog': {'author': {'age': 14, 'score': 9.99, 'name': 'Tom', 'is_child': True}}})
[blog.author]
age = 14
score = 9.99
name = "Tom"
is_child = true
```

Exception
----------

The only exception may occur during parsing: `TomlSyntaxError`.

Specific Notes
--------------

**Each piece of notes bellow comes from [mojombo/toml](https://github.com/mojombo/toml)**, just implemented in toml.py

1. Negative integer and float is ok: `-1` `-0.9`, but positive integer or float in this format is not allowed: `+9` `+8.8`

2. Boolens are always lowercase.

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

6. For float, there must be at least one number on each side of the decimal point.

   ```
   .5  # bad
   ```

7. Datetimes are ISO 8601 dates, only full zulu form is allowed.

   ```
    >>> toml.loads("""date = 1979-05-27T07:32:00Z""")
   {'date': datetime.datetime(1979, 5, 27, 7, 32)}
   ```

8. In strings, all escapes from toml 0.3.1 are supported.

   ```
   \b         - backspace       (U+0008)     [x]
   \t         - tab             (U+0009)     [x]
   \n         - linefeed        (U+000A)     [x]
   \f         - form feed       (U+000C)     [x]
   \r         - carriage return (U+000D)     [x]
   \"         - quote           (U+0022)     [x]
   \\         - backslash       (U+005C)     [x]
   \uXXXX     - unicode         (U+XXXX)     [x]
   \UXXXXXXXX - unicode         (U+XXXXXXXX) [x]
   ```
   ```python
   >>> toml.loads(r"""  # attention to the r here, use raw or unicode or \\\\
   ... path = "C:\\files\\MyPython\\"
   ... """)
   {'path': 'C:\\files\\MyPython\\'}
   ```

9. Multiline strings are supported, as well as trimming whitespace.

   ```toml
   # This will return "The quick brown fox jumps over the lazy dog."""
   key1 = """
   The quick brown \
   fox jumps over \
   the lazy dog."""
   ```

   Literal strings and multiline literal strings are supported.

   ```toml
   # What you see is what you get
   winpath  = 'C:\Users\nodejs\templates'
   winpath2 = '\\ServerX\admin$\system32\'
   quoted   = 'Tom "Dubs" Preston-Werner'
   regex    = '<\i\c*\s*>'
   
   regex2 = '''I [dw]on't need \d{2} apples'''
   lines  = '''
   The first newline is
   trimmed in raw strings.
      All other whitespace
      is preserved.
      '''
   ```

10. The spaces and tabs should be in english mode.(notes for chinese .etc users.)

11. keys can have char `?` and `#`

   ```
   >>> toml.loads(' what? = "Yeah!" ')
   {'what?': 'Yeah!'}
   ```

   ```
   >>> toml.loads(' the# = false  ')
   {'the#': False}
   ```

12. if your `keygroup` ends with no keys:

    ```
    >>> toml.loads("[NoKeysInThisGroup]")                              
    {'NoKeysInThisGroup': {}}                                          
    ```

Tests
-----

So far,  only tested for parser.

    $ nosetests -w tests

TODO
----

2. Unimplemented: Data types may not be mixed. (Later..)

3. which way is better? update already exist key or raise error instead.
