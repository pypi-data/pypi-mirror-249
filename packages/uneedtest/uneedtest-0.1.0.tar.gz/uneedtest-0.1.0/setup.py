# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uneedtest']

package_data = \
{'': ['*']}

install_requires = \
['pyhumps>=3.0']

setup_kwargs = {
    'name': 'uneedtest',
    'version': '0.1.0',
    'description': 'A snake-cased drop in for unittest.TestCase',
    'long_description': "For historical reasons, Python's built-in `unittest` module is not PEP-8\ncompliant. It uses camel case method names instead of snake case names. This\nis not going to change in Python 3. ([1](https://bugs.python.org/issue22250),\n[2](https://discuss.python.org/t/snake-case-aliases-to-camelcased-methods-in-unittest/27381),\n[3](https://stackoverflow.com/questions/17014763/why-are-unittest2-methods-camelcase-if-names-with-underscores-are-preferred))\n\nThis could lead to stylistic inconsistencies, especially if one wants to write\ncustom assertion methods and runs a pep-8 checker over their test code.\n\nTo address this stylistic itch, `uneedtest` offers a simple drop-in\n`TestCase` class which provides snake cased aliases to all the camel cased\nmethods in `unittest.TestCase`.\n\n## Install\n\n    pip install uneedtest\n\n## Use\n\nYou can use `uneedtest.TestCase` in the same way you used to use\n`unittest.TestCase` before. It accepts calls to the corresponding snake case\nmethods. The camel case methods are still working, allowing for gradually fading\nout their use in your test code base:\n\n```python\nfrom uneedtest import TestCase\n\nclass TestMe(TestCase):\n    def test_something(self):\n        self.assert_equal(1, 1)\n        self.assertEqual(1, 1)\n```\n\n## Test\n\nYou can run the tests using [`poetry`](https://python-poetry.org/):\n\n    poetry run pytest\n\nIf you don't want to use `poetry`, you can run the tests with `pytest` or\n`unittest` directly:\n\n    pytest tests/\n",
    'author': 'Jonathan Scholbach',
    'author_email': 'j.scholbach@posteo.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jonathan-scholbach/uneedtest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
