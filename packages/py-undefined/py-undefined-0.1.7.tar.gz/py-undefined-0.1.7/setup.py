# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_undefined']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.9.0,<5.0.0']

setup_kwargs = {
    'name': 'py-undefined',
    'version': '0.1.7',
    'description': 'Provides an Undefined constant.',
    'long_description': '# Py-Undefined\n\n![](https://img.shields.io/badge/License-ApacheV2-blue.svg)\n![](https://img.shields.io/badge/code%20style-black-000000.svg)\n![](https://img.shields.io/pypi/v/py-undefined.svg)\n\nA light-weight library providing an `Undefined` type to Python.\n\n## Install\n\nPy-Undefined is on PyPI and can be installed with:\n\n```shell\npip install py-undefined\n```\n\nOr with [Poetry](https://python-poetry.org/)\n\n```shell\npoetry add py-undefined\n```\n\n## Usage\n\nThe `Undefined` class from this module can be used as a variable type and a value.\n\n```python\nfrom py_undefined import Undefined\n\na: Undefined | int = Undefined\n\nassert a is Undefined\n```\n\n## Why?\n\nThis is very useful to web frameworks that need to distinguish between receiving null\nas a parameter value vs not receiving that parameter at all.\n\n### Example\n\n```python\n# Framework that can now pass `Undefined` instead of `None` to method if param was absent from request.\n@framework.method()\ndef update(a: int | Undefined, b: int | None | Undefined) -> None:\n    if a is not Undefined:\n        ...\n    if b is not Undefined:\n        ...\n```\n\nThis allows for a client to use this method to update only what values are provided.\n\n```python\nmy_client.update(b=1)  # Set b.\nmy_client.update(a=2)  # Set a without setting b to None.\nmy_client.update(b=None)  # b can be set to None explicitly.\n```\n\n## Support The Developer\n\n<a href="https://www.buymeacoffee.com/mburkard" target="_blank">\n  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"\n       width="217"\n       height="60"\n       alt="Buy Me A Coffee">\n</a>\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthew@gburkard.cloud',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/py-undefined',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
