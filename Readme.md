toooml
------

Python parser for [mojombo/toml](https://github.com/mojombo/toml).

Improved version of [marksteve/toml-ply](https://github.com/marksteve/toml-ply)

Support
-------

Version [V0.1](https://github.com/mojombo/toml/blob/master/versions/toml-v0.1.0.md) of toml.


Install
-------

    pip install git+git://github.com/hit9/toooml.git

Use
----

```python
>>> import toooml as toml
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
$ cat some.toml | python -m toooml
{'name': 'Tom'}
$ echo "n = 1.3" | python -m toooml
{'n': 1.3}

```

TODO
----

1. error handle

2. write tests
