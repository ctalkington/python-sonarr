"""Exceptions for Sonarr."""


class SonarrError(Exception):
    """Generic Sonarr Exception."""

    pass


class SonarrConnectionError(SonarrError):
    """Sonarr connection exception."""

    pass


class SonarrAccessRestricted(SonarrError):
    """Sonarr access restricted."""

    pass
