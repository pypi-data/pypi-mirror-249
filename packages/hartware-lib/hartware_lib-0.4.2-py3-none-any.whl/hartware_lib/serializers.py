import json
from dataclasses import is_dataclass
from datetime import datetime
from decimal import Decimal
from functools import partial
from typing import Any, Optional

from hartware_lib.types import AnyDict, ExtraDeserializer, ExtraSerializer


class NoSerializerMatch(Exception):
    pass


class GlobalEncoder(json.JSONEncoder):
    def __init__(
        self,
        *args: Any,
        extra_serializer: Optional[ExtraSerializer] = None,
        **kwargs: Any,
    ):
        super(GlobalEncoder, self).__init__(*args, **kwargs)

        self.extra_serializer = extra_serializer

    def default(self, o: Any) -> AnyDict:
        if self.extra_serializer:
            try:
                return self.extra_serializer(o)
            except NoSerializerMatch:
                pass

        if isinstance(o, datetime):
            return {"_type": o.__class__.__name__, "value": o.isoformat()}
        elif isinstance(o, set):
            return {"_type": o.__class__.__name__, "value": list(o)}
        elif isinstance(o, Decimal):
            return {"_type": o.__class__.__name__, "value": str(o)}
        elif is_dataclass(o):
            return {"_type": o.__class__.__name__, "value": o.__dict__}
        else:
            raise Exception(f"Unknown `{o.__class__.__name__}` type")


def serialize(
    obj: Any,
    indent: Optional[int] = None,
    extra_serializer: Optional[ExtraSerializer] = None,
) -> bytes:
    return (
        GlobalEncoder(indent=indent, extra_serializer=extra_serializer)
        .encode(obj)
        .encode("utf-8")
    )


def _global_decoder(
    obj: AnyDict, extra_deserializer: Optional[ExtraDeserializer]
) -> Any:
    if extra_deserializer:
        try:
            return extra_deserializer(obj)
        except NoSerializerMatch:
            pass

    if obj_type := obj.get("_type"):
        obj_value = obj["value"]

        if obj_type == "set":
            return set(obj_value)
        elif obj_type == "datetime":
            return datetime.fromisoformat(obj_value)
        elif obj_type == "Decimal":
            return Decimal(obj_value)
        else:
            raise Exception(f"Unknown `{obj_type}` type")

    return obj


def deserialize(
    obj: bytes, extra_deserializer: Optional[ExtraDeserializer] = None
) -> Any:
    return json.loads(
        obj, object_hook=partial(_global_decoder, extra_deserializer=extra_deserializer)
    )
