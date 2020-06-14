"""
https://github.com/Sonarr/Sonarr/wiki/Queue
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple

from .base import Base
from .series import Series
from .episode import Episode
from .quality import QualityRevision


@dataclass(frozen=True)
class QueueItem(Base):
    """Object holding queue item information from Sonarr.

    Returned by /queue.
    """

    series: Series
    episode: Episode
    quality: QualityRevision
    size: int
    title: str
    sizeleft: int
    timeleft: timedelta
    estimatedCompletionTime: datetime
    status: str
    trackedDownloadStatus: str
    statusMessages: Tuple[str, ...]
    downloadId: str
    protocol: str
    id: int
