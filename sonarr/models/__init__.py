"""Object model for Sonarr API.

https://github.com/Sonarr/Sonarr/wiki/API
"""
__all__ = [
    "Base",
    "SortKey",
    "SortDirection",
    "PageMixin",
    "CommandStatus",
    "CommandStatusBody",
    "Episode",
    "EpisodeFile",
    "WantedMissing",
    "DownloadData",
    "Download",
    "History",
    "QueueItem",
    "SeriesTitleInfo",
    "ParsedEpisodeInfo",
    "ParseResult",
    "Protocol",
    "Revision",
    "Quality",
    "QualityValue",
    "QualityProfile",
    "QualityProper",
    "QualityRevision",
    "QualityAllowed",
    "QualityAllowedProfile",
    "Release",
    "SeasonStatistics",
    "Season",
    "Rating",
    "AlternateTitle",
    "Image",
    "Tag",
    "Series",
    "DiskSpace",
    "RootFolder",
    "SystemStatus",
    "SystemBackup",
]

from .base import Base, SortKey, SortDirection, Protocol, PageMixin

# /calendar classes in .episode
from .command import CommandStatus, CommandStatusBody  # /command
# /diskspace classes in .system
from .episode import Episode, EpisodeFile, WantedMissing
from .history import DownloadData, Download, History
# TODO Images
# /wanted/missing classes in .episode
from .queue import QueueItem
from .parse import SeriesTitleInfo, ParsedEpisodeInfo, ParseResult
# /profile classes in .quality
from .quality import (
    Revision,
    Quality,
    QualityValue,
    QualityProfile,
    QualityProper,
    QualityRevision,
    QualityAllowed,
    QualityAllowedProfile,
)
from .release import Release
# /release/push classes in .release
# /rootfolder classes in .system
from .series import (
    SeasonStatistics,
    Season,
    Rating,
    AlternateTitle,
    Image,
    Tag,
    Series,
)
# /series/lookup classes in .series
from .system import DiskSpace, RootFolder, SystemStatus, SystemBackup
# /system/status classes in .system
# /system/backup classes in .system
# /tag classes in .series
