For historical reasons, Python's built-in `unittest` module is not PEP-8
compliant. It uses camel case method names instead of snake case names. This
is not going to change in Python 3. ([1](https://bugs.python.org/issue22250),
[2](https://discuss.python.org/t/snake-case-aliases-to-camelcased-methods-in-unittest/27381),
[3](https://stackoverflow.com/questions/17014763/why-are-unittest2-methods-camelcase-if-names-with-underscores-are-preferred))

This could lead to stylistic inconsistencies, especially if one wants to write
custom assertion methods and runs a pep-8 checker over their test code.

To address this stylistic itch, `uneedtest` offers a simple drop-in
`TestCase` class which provides snake cased aliases to all the camel cased
methods in `unittest.TestCase`.

## Install

    pip install uneedtest

## Use

You can use `uneedtest.TestCase` in the same way you used to use
`unittest.TestCase` before. It accepts calls to the corresponding snake case
methods. The camel case methods are still working, allowing for gradually fading
out their use in your test code base:

```python
from uneedtest import TestCase

class TestMe(TestCase):
    def test_something(self):
        self.assert_equal(1, 1)
        self.assertEqual(1, 1)
```

## Test

You can run the tests using [`poetry`](https://python-poetry.org/):

    poetry run pytest

If you don't want to use `poetry`, you can run the tests with `pytest` or
`unittest` directly:

    pytest tests/
