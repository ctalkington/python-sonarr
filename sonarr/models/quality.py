"""
https://github.com/Sonarr/Sonarr/wiki/Profile
"""
from dataclasses import dataclass
from typing import Tuple, Optional

from .base import Base


@dataclass(frozen=True)
class Quality(Base):
    """Quality definition.

    Attribute of QualityRevision, QualityProper, QualityAllowed, QualityAllowedProfile
    """

    id: int
    name: Optional[str] = None
    source: Optional[str] = None
    resolution: Optional[int] = None
    weight: Optional[int] = None


@dataclass(frozen=True)
class Revision(Base):
    """Attribute of QualityRevision
    """

    version: int
    real: int


@dataclass(frozen=True)
class QualityRevision(Base):
    """Attribute of Download, QueueItem.
    """

    quality: Quality
    revision: Revision


@dataclass(frozen=True)
class QualityValue(Base):
    """Quality value configuration.

    Attribute of QualityProfile
    """

    name: str
    allowed: Tuple[Quality, ...]
    cutoff: Quality
    id: int


@dataclass(frozen=True)
class QualityProfile(Base):
    """Quality profile configuration.

    Attribute of Series (in /calendar, /wanted/missing).
    """

    value: QualityValue
    isLoaded: bool


@dataclass(frozen=True)
class QualityProper(Base):
    """Quality report.

    Attribute of EpisodeFile, Release.
    """

    quality: Quality
    proper: bool


@dataclass(frozen=True)
class QualityAllowed(Base):
    """Attribute of QualityAllowedProfile.
    """

    quality: Quality
    allowed: bool


@dataclass(frozen=True)
class QualityAllowedProfile(Base):
    """Returned by /profile.
    """

    name: str
    cutoff: Quality
    items: Tuple[QualityAllowed, ...]
    id: int
    language: Optional[str] = None
