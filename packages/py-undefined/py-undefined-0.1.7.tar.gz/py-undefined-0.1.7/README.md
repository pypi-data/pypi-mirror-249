# Py-Undefined

![](https://img.shields.io/badge/License-ApacheV2-blue.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)
![](https://img.shields.io/pypi/v/py-undefined.svg)

A light-weight library providing an `Undefined` type to Python.

## Install

Py-Undefined is on PyPI and can be installed with:

```shell
pip install py-undefined
```

Or with [Poetry](https://python-poetry.org/)

```shell
poetry add py-undefined
```

## Usage

The `Undefined` class from this module can be used as a variable type and a value.

```python
from py_undefined import Undefined

a: Undefined | int = Undefined

assert a is Undefined
```

## Why?

This is very useful to web frameworks that need to distinguish between receiving null
as a parameter value vs not receiving that parameter at all.

### Example

```python
# Framework that can now pass `Undefined` instead of `None` to method if param was absent from request.
@framework.method()
def update(a: int | Undefined, b: int | None | Undefined) -> None:
    if a is not Undefined:
        ...
    if b is not Undefined:
        ...
```

This allows for a client to use this method to update only what values are provided.

```python
my_client.update(b=1)  # Set b.
my_client.update(a=2)  # Set a without setting b to None.
my_client.update(b=None)  # b can be set to None explicitly.
```

## Support The Developer

<a href="https://www.buymeacoffee.com/mburkard" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"
       width="217"
       height="60"
       alt="Buy Me A Coffee">
</a>
