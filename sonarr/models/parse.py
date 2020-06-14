"""
https://github.com/Sonarr/Sonarr/wiki/Parse
"""
from dataclasses import dataclass
from typing import Tuple, Optional

from .base import Base
from .episode import Episode
from .series import Series
from .quality import QualityRevision


@dataclass(frozen=True)
class SeriesTitleInfo(Base):
    """Attribute of ParsedEpisodeInfo."""

    title: str
    titleWithoutYear: str
    year: int


@dataclass(frozen=True)
class ParsedEpisodeInfo(Base):
    """Attribute of ParseResult."""

    releaseTitle: str
    seriesTitle: str
    seriesTitleInfo: SeriesTitleInfo
    quality: QualityRevision
    seasonNumber: int
    episodeNumbers: Tuple[int, ...]
    absoluteEpisodeNumbers: Tuple[int, ...]
    language: str
    fullSeason: bool
    special: bool
    releaseGroup: str
    releaseHash: str
    isDaily: bool
    isAbsoluteNumbering: bool
    isPossibleSpecialEpisode: bool


@dataclass(frozen=True)
class ParseResult(Base):
    """Returns the result of parsing a title or path.
    Series and episodes will be returned only if the parsing matches to a
    specific series and one or more episodes.

    Returned by /parse.
    """

    title: str
    parsedEpisodeInfo: ParsedEpisodeInfo
    episodes: Tuple[Episode, ...]
    series: Optional[Series] = None
