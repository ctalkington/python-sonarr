"""
https://github.com/Sonarr/Sonarr/wiki/Release
https://github.com/Sonarr/Sonarr/wiki/Release-Push
"""
from dataclasses import dataclass
from typing import Tuple
from datetime import datetime

from .base import Base
from .quality import QualityProper


@dataclass(frozen=True)
class Release(Base):
    """Returned by /release."""

    guid: str
    quality: QualityProper
    age: int
    size: int
    indexerId: int
    indexer: str
    releaseGroup: str
    title: str
    fullSeason: bool
    sceneSource: bool
    seasonNumber: int
    language: str
    seriesTitle: str
    episodeNumbers: Tuple[int, ...]
    approved: bool
    tvRageId: int
    rejections: Tuple[str, ...]
    publishDate: datetime
    downloadUrl: str
    downloadAllowed: bool
