from __future__ import (
    annotations,
)

from ._core import (
    JsonObj,
    JsonValue,
)
from dataclasses import (
    dataclass,
)
from deprecated import (
    deprecated,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
    Primitive,
)
from fa_purity.result import (
    Result,
)
from fa_purity.result.core import (
    ResultE,
)
from fa_purity.utils import (
    cast_exception,
    raise_exception,
)
import simplejson
from typing import (
    Any,
    cast,
    Dict,
    IO,
    List,
    Optional,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
UnfoldedJVal = Union[Primitive, JsonPrimitive, JsonObj, FrozenList[JsonValue]]


class _HandledException(Exception):
    pass


@dataclass(frozen=True)
class JsonValueFactory:
    "Factory of `JsonValue` objects"

    @staticmethod
    def from_unfolded(raw: UnfoldedJVal) -> JsonValue:
        if isinstance(raw, tuple):
            return JsonValue.from_list(raw)
        if isinstance(raw, FrozenDict):
            return JsonValue.from_json(raw)
        if isinstance(raw, JsonPrimitive):
            return JsonValue.from_primitive(raw)
        return JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(raw))

    @staticmethod
    def from_list(
        raw: Union[List[Primitive], FrozenList[Primitive]]
    ) -> JsonValue:
        return JsonValue.from_list(UnfoldedFactory.from_list(raw))

    @staticmethod
    def from_dict(
        raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
    ) -> JsonValue:
        return JsonValue.from_json(UnfoldedFactory.from_dict(raw))

    @classmethod
    def from_any(cls, raw: Optional[_T]) -> ResultE[JsonValue]:
        if isinstance(raw, (FrozenDict, dict)):
            try:
                json_dict = FrozenDict(
                    {
                        JsonPrimitiveFactory.from_any(key)
                        .bind(JsonPrimitiveUnfolder.to_str)
                        .alt(_HandledException)
                        .alt(raise_exception)
                        .unwrap(): cls.from_any(val)
                        .alt(_HandledException)
                        .alt(raise_exception)
                        .unwrap()
                        for key, val in raw.items()
                    }
                )
                return Result.success(JsonValue.from_json(json_dict))
            except _HandledException as err:
                return Result.failure(cast_exception(err))
        if isinstance(raw, (list, tuple)):
            try:
                json_list = tuple(
                    cls.from_any(item)
                    .alt(_HandledException)
                    .alt(raise_exception)
                    .unwrap()
                    for item in raw
                )
                return Result.success(JsonValue.from_list(json_list))
            except _HandledException as err:
                return Result.failure(cast_exception(err))
        return JsonPrimitiveFactory.from_any(raw).map(JsonValue.from_primitive)

    @staticmethod
    @deprecated("[Moved]: use `UnfoldedFactory.loads` instead")  # type: ignore[misc]
    def loads(raw: str) -> ResultE[JsonObj]:
        raw_json = cast(Dict[str, Any], simplejson.loads(raw))  # type: ignore[misc]
        return UnfoldedFactory.from_raw_dict(raw_json)  # type: ignore[misc]

    @staticmethod
    @deprecated("[Moved]: use `UnfoldedFactory.load` instead")  # type: ignore[misc]
    def load(raw: IO[str]) -> ResultE[JsonObj]:
        raw_json = cast(Dict[str, Any], simplejson.load(raw))  # type: ignore[misc]
        return UnfoldedFactory.from_raw_dict(raw_json)  # type: ignore[misc]


@dataclass(frozen=True)
class UnfoldedFactory:
    "Factory of unfolded `JsonValue` objects"

    @staticmethod
    def from_list(
        raw: Union[List[Primitive], FrozenList[Primitive]]
    ) -> FrozenList[JsonValue]:
        return tuple(
            JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(item))
            for item in raw
        )

    @staticmethod
    def from_dict(
        raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
    ) -> JsonObj:
        return FrozenDict(
            {
                key: JsonValue.from_primitive(
                    JsonPrimitiveFactory.from_raw(val)
                )
                for key, val in raw.items()
            }
        )

    @staticmethod
    def from_unfolded_dict(
        raw: Union[Dict[str, UnfoldedJVal], FrozenDict[str, UnfoldedJVal]]
    ) -> JsonObj:
        return FrozenDict(
            {
                key: JsonValueFactory.from_unfolded(val)
                for key, val in raw.items()
            }
        )

    @staticmethod
    def from_unfolded_list(
        raw: Union[List[UnfoldedJVal], FrozenList[UnfoldedJVal]]
    ) -> FrozenList[JsonValue]:
        return tuple(JsonValueFactory.from_unfolded(item) for item in raw)

    @staticmethod
    def from_raw_dict(raw: Dict[str, Any]) -> ResultE[JsonObj]:  # type: ignore[misc]
        err = Result.failure(
            cast_exception(TypeError("Not a `JsonObj`")), JsonObj
        )
        return JsonValueFactory.from_any(raw).bind(  # type: ignore[misc]
            lambda jv: jv.map(
                lambda _: err,
                lambda _: err,
                lambda x: Result.success(x),
            )
        )

    @classmethod
    def loads(cls, raw: str) -> ResultE[JsonObj]:
        raw_json = cast(Dict[str, Any], simplejson.loads(raw))  # type: ignore[misc]
        return cls.from_raw_dict(raw_json)  # type: ignore[misc]

    @classmethod
    def load(cls, raw: IO[str]) -> ResultE[JsonObj]:
        raw_json = cast(Dict[str, Any], simplejson.load(raw))  # type: ignore[misc]
        return cls.from_raw_dict(raw_json)  # type: ignore[misc]
