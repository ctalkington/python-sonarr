"""Tests for sonarr.models.base."""
from dataclasses import dataclass
from datetime import datetime, date, time, timedelta, timezone
from enum import Enum
from typing import Optional, Tuple

import pytest
import sonarr.models as models


UTC = timezone.utc


@dataclass(frozen=True)
class MockModel(models.Base):
    foo: int
    bar: Optional[str] = None


@dataclass(frozen=True)
class MockModel2(models.Base):
    foo: int
    bar: Optional[MockModel] = None


@dataclass(frozen=True)
class NestedModel(models.Base):
    foo: MockModel
    bar: Optional[MockModel]
    baz: Tuple[MockModel, ...]


class MockEnum(Enum):
    FOO = "foo"
    BAR = "bar"


def test_base():
    """Test model Base class."""
    # __init__() mandatory attributes
    assert MockModel(foo=1, bar="one").foo == 1
    with pytest.raises(TypeError):
        MockModel(bar="one")

    # __init__() optional attributes
    assert MockModel(foo=1).bar is None

    # from_dict() doesn't work on base class, only subclasses.
    with pytest.raises(NotImplementedError):
        attrs = {"foo": 1, "bar": 2}
        models.Base.from_dict(attrs)

    # to_dict() doesn't work on base class, only subclasses.
    with pytest.raises(NotImplementedError):
        instance = models.Base()
        instance.to_dict()


def test_encode_datetime():
    """Test encode_datetime()."""
    # "Zulu time" for UTC
    encoded = models.base.encode_datetime(
        datetime(2020, 6, 5, 13, 38, 55, tzinfo=UTC)
    )
    assert encoded == "2020-06-05T13:38:55Z"

    # TZ naive
    encoded = models.base.encode_datetime(
        datetime(2020, 6, 5, 13, 38, 55)
    )
    assert encoded == "2020-06-05T13:38:55Z"

    # microseconds
    encoded = models.base.encode_datetime(
        datetime(2020, 6, 5, 13, 38, 55, 123456, tzinfo=UTC)
    )
    assert encoded == "2020-06-05T13:38:55.123456Z"


def test_encode_date():
    """Test encode_date()."""
    encoded = models.base.encode_date(date(2020, 6, 5))
    assert encoded == "2020-06-05"


def test_encode_time():
    """Test encode_time()."""
    # Whole seconds
    encoded = models.base.encode_time(time(13, 38, 55))
    assert encoded == "13:38:55"

    # microseconds
    encoded = models.base.encode_time(time(13, 38, 55, 123456))
    assert encoded == "13:38:55.123456"


def test_encode_timedelta():
    """Test encode_timedelta()."""
    # Whole seconds
    encoded = models.base.encode_timedelta(
        timedelta(hours=13, minutes=38, seconds=55)
    )
    assert encoded == "13:38:55"


def test_encode_tuple():
    """Test encode_tuple()."""
    # tuple of int
    vals = (1, 2, 3)
    encoded = models.base.encode_tuple(vals)
    assert encoded == [1, 2, 3]

    # tuple of str
    vals = ("abc", "def")
    encoded = models.base.encode_tuple(vals)
    assert encoded == ["abc", "def"]

    # tuple of dict
    vals = (
        {
            "bool": True,
            "int": 1,
            "float": 2.0,
            "str": "abc",
            "datetime": datetime(2020, 6, 5, 13, 38, 55, 123456, tzinfo=UTC),
            "date": date(2020, 6, 5),
            "time": time(13, 38, 55),
            "timedelta": timedelta(hours=13, minutes=38, seconds=55),
            "tuple": (1, 2, 3),
            "dict": {"foo": True, "bar": 1},
        },
        {
            "bool": False,
            "int": 2,
            "float": 3.0,
            "str": "def",
            "datetime": datetime(2020, 6, 5, 13, 38, 55, 234567, tzinfo=UTC),
            "date": date(2020, 6, 6),
            "time": time(13, 38, 56),
            "timedelta": timedelta(hours=13, minutes=38, seconds=56),
            "tuple": (4, 5, 6),
            "dict": {"foo": False, "bar": 2},
        },
    )
    encoded = models.base.encode_tuple(vals)
    assert isinstance(encoded, list)
    assert len(encoded) == 2
    val0, val1 = encoded

    assert val0 == {
        "bool": True,
        "int": 1,
        "float": 2.0,
        "str": "abc",
        "datetime": "2020-06-05T13:38:55.123456Z",
        "date": "2020-06-05",
        "time": "13:38:55",
        "timedelta": "13:38:55",
        "tuple": [1, 2, 3],
        "dict": {"foo": True, "bar": 1},
    }

    assert val1 == {
        "bool": False,
        "int": 2,
        "float": 3.0,
        "str": "def",
        "datetime": "2020-06-05T13:38:55.234567Z",
        "date": "2020-06-06",
        "time": "13:38:56",
        "timedelta": "13:38:56",
        "tuple": [4, 5, 6],
        "dict": {"foo": False, "bar": 2},
    }


def test_encode_dict():
    """Test encode_dict()."""
    encoded = models.base.encode_dict(
        {
            "bool": True,
            "int": 1,
            "float": 2.0,
            "str": "abc",
            "datetime": datetime(2020, 6, 5, 13, 38, 55, 123456, tzinfo=UTC),
            "date": date(2020, 6, 5),
            "time": time(13, 38, 55),
            "timedelta": timedelta(hours=13, minutes=38, seconds=55),
            "tuple": (1, 2, 3),
            "dict": {"foo": True, "bar": 1},
        }
    )
    assert encoded == {
        "bool": True,
        "int": 1,
        "float": 2.0,
        "str": "abc",
        "datetime": "2020-06-05T13:38:55.123456Z",
        "date": "2020-06-05",
        "time": "13:38:55",
        "timedelta": "13:38:55",
        "tuple": [1, 2, 3],
        "dict": {"foo": True, "bar": 1},
    }


def test_decode_list_to_tuple():
    """Test decode_list_to_tuple()."""
    # List[bool] -> Tuple[bool]
    decoded = models.base.decode_list_to_tuple(bool, [True, False, False])
    assert decoded == (True, False, False)

    # List[int] -> Tuple[int]
    decoded = models.base.decode_list_to_tuple(int, [3, 1, 2])
    assert decoded == (3, 1, 2)

    # List[float] -> Tuple[float]
    decoded = models.base.decode_list_to_tuple(float, [3.0, 1.1, 2.5])
    assert decoded == (3.0, 1.1, 2.5)

    # List[str] -> Tuple[str]
    decoded = models.base.decode_list_to_tuple(str, ["foo", "bar", "baz"])
    assert decoded == ("foo", "bar", "baz")

    # List[JSON datetime] -> Tuple[Python datetime]
    decoded = models.base.decode_list_to_tuple(
        datetime, [
            "1960-02-15T06:00:00Z",
            "2016-02-05T16:40:11.614176Z",
            "2008-02-04T13:44:24.204583Z",
        ]
    )

    assert decoded == (
        datetime(1960, 2, 15, 6, tzinfo=UTC),
        datetime(2016, 2, 5, 16, 40, 11, 614176, tzinfo=UTC),
        datetime(2008, 2, 4, 13, 44, 24, 204583, tzinfo=UTC),
    )


def test_decode_optional():
    """Test decode_optional()."""
    # Optional basic type
    for typ in (bool, int, float, str):
        decoded = models.base.decode_optional(type, None)

    assert models.base.decode_optional(bool, True) is True
    assert models.base.decode_optional(int, 1) == 1
    assert models.base.decode_optional(float, 1.0) == 1.0
    assert models.base.decode_optional(str, "foo") == "foo"

    # Optional model
    decoded = models.base.decode_optional(MockModel, None)
    assert decoded is None

    decoded = models.base.decode_optional(MockModel, {'foo': 1, 'bar': 'one'})
    assert decoded == MockModel(foo=1, bar="one")


def test_decode_model():
    """Test decode_model()."""
    decoded = models.base.decode_model(MockModel, {'foo': 123, 'bar': 'baz'})
    assert decoded == MockModel(foo=123, bar='baz')

    # Missing optional attribute
    decoded = models.base.decode_model(MockModel, {'foo': 123})
    assert decoded == MockModel(foo=123, bar=None)

    # Nested model
    decoded = models.base.decode_model(
        NestedModel,
        {
            'foo': {'foo': 1, 'bar': 'one'},
            'bar': {'foo': 2, 'bar': 'two'},
            'baz': [
                {'foo': 3, 'bar': 'three'},
                {'foo': 4, 'bar': 'four'},
            ]
        }
    )
    inner1 = MockModel(foo=1, bar="one")
    inner2 = MockModel(foo=2, bar="two")
    inner3 = MockModel(foo=3, bar="three")
    inner4 = MockModel(foo=4, bar="four")
    instance = NestedModel(foo=inner1, bar=inner2, baz=(inner3, inner4))

    assert type(decoded) == type(instance)
    # FIXME - dataclass default __eq__() not doing the job here
    #  assert decoded == instance


def test_decode_enum():
    """Test decode_enum()."""
    assert models.base.decode_enum(MockEnum, "foo") == MockEnum.FOO
    assert models.base.decode_enum(MockEnum, "bar") == MockEnum.BAR
    with pytest.raises(KeyError):
        models.base.decode_enum(MockEnum, "baz")


def test_decode_basic():
    """Test decode_basic().

    This should pass through unchanged the fundamental data types that
    json.JSONDecoder handles correctly, i.e.  [bool, int, float, str].
    """
    # bool
    decoded = models.base.decode_basic(bool, True)
    assert type(decoded) is bool
    assert decoded is True

    # int
    decoded = models.base.decode_basic(int, 3)
    assert type(decoded) is int
    assert decoded == 3

    # float
    decoded = models.base.decode_basic(float, 1.1)
    assert type(decoded) is float
    assert decoded == 1.1

    # str
    decoded = models.base.decode_basic(str, "foo")
    assert type(decoded) is str
    assert decoded == "foo"


def test_decode_datetime():
    """Test decode_datetime()."""
    # "Zulu time" for UTC
    decoded = models.base.decode_datetime(datetime, "2020-06-05T13:38:55Z")
    assert decoded == datetime(2020, 6, 5, 13, 38, 55, tzinfo=UTC)

    # Values to decode must be formatted as Zulu time!
    with pytest.raises(AssertionError):
        models.base.decode_datetime(datetime, "2020-06-05T13:38:55")

    # milliseconds
    decoded = models.base.decode_datetime(datetime, "2020-06-05T13:38:55.123Z")
    assert decoded == datetime(2020, 6, 5, 13, 38, 55, 123000, tzinfo=UTC)

    # microseconds
    decoded = models.base.decode_datetime(datetime, "2020-06-05T13:38:55.123456Z")
    assert decoded == datetime(2020, 6, 5, 13, 38, 55, 123456, tzinfo=UTC)

    # weird fractional seconds
    decoded = models.base.decode_datetime(datetime, "2020-06-05T13:38:55.1234Z")
    assert decoded == datetime(2020, 6, 5, 13, 38, 55, 123400, tzinfo=UTC)

    decoded = models.base.decode_datetime(datetime, "2020-06-05T13:38:55.1234567Z")
    assert decoded == datetime(2020, 6, 5, 13, 38, 55, 123457, tzinfo=UTC)


def test_decode_date():
    """Test decode_date()."""
    decoded = models.base.decode_date(date, "2020-06-05")
    assert decoded == date(2020, 6, 5)


def test_decode_time():
    """Test decode_time()."""
    # Whole seconds
    decoded = models.base.decode_time(time, "13:38:55")
    assert decoded == time(13, 38, 55)

    # milliseconds
    decoded = models.base.decode_time(time, "13:38:55.123")
    assert decoded == time(13, 38, 55, 123000)

    # microseconds
    decoded = models.base.decode_time(time, "13:38:55.123456")
    assert decoded == time(13, 38, 55, 123456)


def test_decode_timedelta():
    """Test decode_time()."""
    # Whole seconds
    decoded = models.base.decode_timedelta(timedelta, "13:38:55")
    assert decoded == timedelta(hours=13, minutes=38, seconds=55)
