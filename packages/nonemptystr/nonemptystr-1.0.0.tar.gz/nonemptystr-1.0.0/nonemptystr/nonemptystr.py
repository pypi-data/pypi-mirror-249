from __future__ import annotations

from typing import Any

try:
    from pydantic_core import core_schema
except ImportError:
    pass

from .exceptions import EmptyString


class nonemptystr(str):
    def __new__(cls, obj: object) -> nonemptystr:
        s = str(obj)
        if not s:
            raise EmptyString("string is empty")
        return str.__new__(nonemptystr, s)

    # for pydantic
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        try:
            return core_schema.no_info_after_validator_function(cls, handler(str))
        except NameError:
            raise RuntimeError(
                "cannot import core_schema from pydantic_core, install Pydantic to use nonemptystr with Pydantic",
            ) from None

    # for pydantic
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: Any) -> Any:
        json_schema = handler(core_schema)
        json_schema.update(minLength=1)
        return json_schema
