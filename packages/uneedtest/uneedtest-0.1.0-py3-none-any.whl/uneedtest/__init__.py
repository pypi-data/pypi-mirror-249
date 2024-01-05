from typing import Any, ClassVar
from unittest import TestCase as UnitTestCase

from humps import decamelize


class TestCase(UnitTestCase):
    __redirect: ClassVar[dict[str, str]] = {
        decamelize(legacy_attr): legacy_attr
        for legacy_attr in dir(UnitTestCase)
        if not legacy_attr.startswith("_")
    }

    @classmethod
    def add_class_cleanup(cls, *args, **kwargs) -> None:
        cls.addClassCleanup(*args, **kwargs)

    def __init_subclass__(cls) -> None:
        for legacy_method in [
            "setUpClass",
            "tearDownClass",
            "doClassCleanups",
        ]:
            method = decamelize(legacy_method)
            if hasattr(cls, method):
                setattr(cls, legacy_method, getattr(cls, method))
        return super().__init_subclass__()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for legacy_method in ["setUp", "tearDown", "addCleanup", "doCleanups"]:
            method = decamelize(legacy_method)
            if hasattr(self, method):
                setattr(self, legacy_method, getattr(self, method))

    def __getattr__(self, name: str) -> Any:
        if camelized_name := self.__redirect.get(name):
            name = camelized_name
        return super().__getattribute__(name)


__all__ = ["TestCase"]
