"""Exceptions for Sonarr."""


class SonarrError(Exception):
    """Generic Sonarr Exception."""

    pass


class SonarrConnectionError(SonarrError):
    """Sonarr connection exception."""

    pass


class SonarrAccessRestricted(SonarrError):
    """Sonarr access restricted exception."""

    pass


class SonarrResourceNotFound(SonarrError):
    """Sonarr resource not found exception."""

    pass
