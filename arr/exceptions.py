"""Exceptions for Arr based systems."""


class ArrError(Exception):
    """Generic Arr Exception."""
    pass


class ArrConnectionError(ArrError):
    """Arr connection exception."""
    pass


class ArrAccessRestricted(ArrError):
    """Arr access restricted exception."""
    pass


class ArrResourceNotFound(ArrError):
    """Arr resource not found exception."""
    pass
