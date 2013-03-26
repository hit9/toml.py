toml.py
------

Python parser for [mojombo/toml](https://github.com/mojombo/toml).

Improved version of [marksteve/toml-ply](https://github.com/marksteve/toml-ply)

Support
-------

Version [V0.1](https://github.com/mojombo/toml/blob/master/versions/toml-v0.1.0.md) of toml.


Install
-------

    pip install git+git://github.com/hit9/toml.py.git

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
... name = "\u6c64\u59c6"
... """)
{u'name': u'\u6c64\u59c6'}
```

Empty input:

```python
>>> toml.loads("")
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

**Each piece of notes bellow come from [mojombo/toml](https://github.com/mojombo/toml)**,just implemented in toml.py

1. Negative integer and float is ok: `-1 -0.9`, but positive integer or float in this format is not allowed: `+9` `+8.8`

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

TODO
----

1. error handle

2. write tests

3. doc for specific about array(comma),+9 balabala

4. to fix:Data types may not be mixed.
