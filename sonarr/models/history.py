"""
https://github.com/Sonarr/Sonarr/wiki/History
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Optional

from .base import Base, PageMixin
from .episode import Episode
from .series import Series
from .quality import QualityRevision


@dataclass(frozen=True)
class DownloadData(Base):
    """Attribute of Download.
    """

    droppedPath: Optional[str] = None
    importedPath: Optional[str] = None
    downloadClient: Optional[str] = None
    reason: Optional[str] = None
    indexer: Optional[str] = None
    nzbInfoUrl: Optional[str] = None
    releaseGroup: Optional[str] = None
    age: Optional[str] = None
    ageHours: Optional[str] = None
    ageMinutes: Optional[str] = None
    publishedDate: Optional[datetime] = None
    size: Optional[str] = None
    downloadUrl: Optional[str] = None
    guid: Optional[str] = None
    tvdbId: Optional[str] = None
    tvRageId: Optional[str] = None
    protocol: Optional[str] = None


@dataclass(frozen=True)
class Download(Base):
    """Episode download report.

    Attribute of History.
    """

    episodeId: int
    seriesId: int
    sourceTitle: str
    quality: QualityRevision
    qualityCutoffNotMet: bool
    date: datetime
    eventType: str
    data: DownloadData
    episode: Episode
    series: Series
    id: int
    downloadId: Optional[str] = None


@dataclass(frozen=True)
class History(Base, PageMixin):
    """Page of episode download history.

    Returned by /history.
    """
    records: Tuple[Download, ...]
