"""
"""

import dataclasses
from dataclasses import dataclass
from typing import Tuple, Optional, Union
from datetime import date, datetime, time, timedelta, timezone
import enum


_NoneType = type(None)
UTC = timezone.utc


class Base:
    """Base class for Sonarr API JSON objects."""

    def to_dict(self):
        if type(self) is Base:
            raise NotImplementedError("Don't use base class, only subclasses.")

        encoded = encode_dict(dataclasses.asdict(self))
        return encoded

    @classmethod
    def from_dict(cls, data: dict) -> "Base":
        if cls is Base:
            raise NotImplementedError("Don't use base class, only subclasses.")

        try:
            classtypes = {fld.name: fld.type for fld in dataclasses.fields(cls)}
        except TypeError:
            raise TypeError(f"{cls.__name__} must be a dataclasses.dataclass")

        decoded = {}
        for attr, val in data.items():
            if attr not in classtypes:
                msg = (f"{cls.__name__}.from_dict() got an unexpected keyword "
                       f"argument {attr}={val}")
                raise TypeError(msg)

            attr_type = classtypes[attr]

            try:
                if hasattr(attr_type, "__origin__"):
                    # Generic type from ``typing`` module
                    attr_type, decoder = make_decoder_generic(attr_type)
                else:
                    decoder = make_decoder_specific(attr_type)

                decoded_val = decoder(attr_type, val)
            except Exception as err:
                errmsg = err.args[0]
                msg = f"{cls.__name__}.{attr}(type {attr_type})={val}: {errmsg}"
                raise ValueError(msg)

            decoded[attr] = decoded_val

        try:
            instance = cls(**decoded)
        except Exception as e:
            msg = f"{cls.__name__}.from_dict() failed: " + e.args[0]
            raise ValueError(msg)
        return instance


def encode_basic(val: Union[bool, int, float, str]) -> Union[bool, int, float, str]:
    return val


def encode_datetime(val: datetime) -> str:
    """ "Zulu" milspeak for UTC"""
    encoded = val.replace(tzinfo=None).isoformat()
    return encoded + "Z"


def encode_date(val: date) -> str:
    encoded = val.isoformat()
    return encoded


def encode_time(val: time) -> str:
    encoded = val.replace(tzinfo=None).isoformat()
    return encoded


def encode_timedelta(val: timedelta) -> str:
    minutes, seconds = divmod(val.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    encoded = f"{hours:02}:{minutes:02}:{seconds:02}"
    return encoded


def encode_tuple(val: tuple) -> list:
    encoded = [TYPE_ENCODERS[type(v)](v) for v in val]
    return encoded


def encode_dict(val: dict) -> dict:
    def enc(v):
        if isinstance(v, enum.Enum):
            v_enc = v.value
        else:
            encoder = TYPE_ENCODERS[type(v)]
            v_enc = encoder(v)
        return v_enc

    return {attr: enc(v) for attr, v in val.items()}


TYPE_ENCODERS = {
    _NoneType: encode_basic,
    bool: encode_basic,
    int: encode_basic,
    float: encode_basic,
    str: encode_basic,
    datetime: encode_datetime,
    date: encode_date,
    time: encode_time,
    timedelta: encode_timedelta,
    tuple: encode_tuple,
    dict: encode_dict,
}


def make_decoder_generic(attr_type):
    origin = attr_type.__origin__
    args = attr_type.__args__
    # Sonarr API models only use:
    #   - variable length Tuple of homogenous type Tuple[str, ...]
    #   - Optional type Union[str, NoneType]
    if origin is tuple:
        if len(args) != 2 or args[-1] is not Ellipsis:
            raise ValueError("Tuple attribute definition must contain Ellipsis")

        attr_type = args[0]
        decoder = decode_list_to_tuple
    else:
        assert origin is Union
        if len(args) != 2 or args[-1] is not _NoneType:
            raise ValueError("Union attribute definition only allowed as Optional")

        attr_type = args[0]
        decoder = decode_optional

    return attr_type, decoder


def decode_list_to_tuple(attr_type, val: list) -> Tuple:
    decoder = make_decoder_specific(attr_type)
    return tuple(decoder(attr_type, item) for item in val)


def decode_optional(attr_type, val) -> Optional:
    if val is None:
        return None
    elif issubclass(attr_type, Base) and len(val) == 0:
        return None

    decoder = make_decoder_specific(attr_type)
    return decoder(attr_type, val)


def make_decoder_specific(attr_type):
    if issubclass(attr_type, Base):
        return decode_model
    elif issubclass(attr_type, enum.Enum):
        return decode_enum
    else:
        assert attr_type in TYPE_DECODERS
        return TYPE_DECODERS[attr_type]


def decode_model(attr_type: Base, val: dict) -> Base:
    return attr_type.from_dict(val)


def decode_enum(attr_type: enum.Enum, val) -> enum.Enum:
    members = {member.value: member for member in attr_type}
    return members[val]


def decode_basic(attr_type, val) -> Union[bool, int, float, str]:
    # There's some slop in the Sonarr API w/r/t int vs. float
    # e.g. models.series.SeasonStatistics.percentOfEpisodes
    return attr_type(val)


def decode_datetime(attr_type, val) -> datetime:
    return _datetime_fromisoformat(val)


def decode_date(attr_type, val) -> date:
    return date.fromisoformat(val)


def decode_time(attr_type, val) -> time:
    return time.fromisoformat(val)


def decode_timedelta(attr_type, val) -> timedelta:
    # datetime.timedelta lacks a parsing constructor, so reuse
    # datetime.time.fromisoformat() and cast as datetime.timedelta.
    tm = time.fromisoformat(val)
    return timedelta(hours=tm.hour, minutes=tm.minute, seconds=tm.second)


TYPE_DECODERS = {
    bool: decode_basic,
    int: decode_basic,
    float: decode_basic,
    str: decode_basic,
    datetime: decode_datetime,
    date: decode_date,
    time: decode_time,
    timedelta: decode_timedelta,
}


@enum.unique
class SortKey(enum.Enum):
    SERIESTITLE = "series.title"
    DATE = "date"
    AIRDATE = "airDateUtc"


@enum.unique
class SortDirection(enum.Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


@enum.unique
class Protocol(enum.Enum):
    USENET = "Usenet"
    TORRENT = "Torrent"


@dataclass(frozen=True)
class PageMixin:
    """Mixin implementing interface for paginated records.
    """
    page: int
    pageSize: int
    sortKey: SortKey
    sortDirection: SortDirection
    totalRecords: int
    records: NotImplemented  # Implement in subclasses


def _datetime_fromisoformat(dt_str: str) -> datetime:
    """Parse ISO-8601 datetime strings as provided by Sonarr's API.

    Specifically handle:
        * "Zulu" milspeak for UTC
        * fractional seconds other than exactly 3 or 6 digits (milli/microseconds)

    ... all of which are legal per ISO-8601 and used by Sonarr's API, but blow up
    datetime.datetime.fromisoformat().

    N.B. a more general solution is to use the dateutil package to parse ISO-8601,
    but the dependency seems like overkill given the stability and predictability
    of Sonarr's APi in this regard.
    """
    # "Zulu" milspeak for UTC
    # HACK - brittle inelegant hardcode
    assert dt_str.endswith("Z")
    dt_str = dt_str[:-1]

    # datetime.datetime.fromisoformat() blows up if fractional seconds don't
    # have exactly 3 or 6 digits.
    #
    # datetime.datetime.strptime() zero-pads (on the right) fractional seconds
    # with fewer than 6 digits (good) but still blows up if fractional seconds
    # have more than 6 digits (bad).
    #
    # Sonarr API returns fractional seconds with arbitrary digits, so we need
    # to parse them manually.
    if "." in dt_str:
        dt_str, frac_sec = dt_str.split(".")
        num_digits = len(frac_sec)
        microsecond = round(int(frac_sec) / 10**(num_digits - 6))
    else:
        microsecond = 0

    dt = datetime.fromisoformat(dt_str)
    return dt.replace(microsecond=microsecond, tzinfo=UTC)
