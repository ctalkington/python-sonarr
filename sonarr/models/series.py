"""
https://github.com/Sonarr/Sonarr/wiki/Series
https://github.com/Sonarr/Sonarr/wiki/Series-Lookup
"""
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime, time

from .base import Base
from .quality import QualityProfile


@dataclass(frozen=True)
class SeasonStatistics(Base):
    """Attribute of Season.
    """
    episodeFileCount: int
    episodeCount: int
    totalEpisodeCount: int
    sizeOnDisk: int
    percentOfEpisodes: float
    #  percentOfEpisodes: int
    previousAiring: Optional[datetime] = None
    nextAiring: Optional[datetime] = None


@dataclass(frozen=True)
class Season(Base):
    """TV series season metadata.

    Attribute of Series.
    """
    seasonNumber: int
    monitored: bool
    statistics: Optional[SeasonStatistics] = None


@dataclass(frozen=True)
class Rating(Base):
    """Attribute of Series"""
    votes: int
    value: float


@dataclass(frozen=True)
class AlternateTitle(Base):
    """Attribute of Series"""
    title: str
    seasonNumber: Optional[int] = None
    sceneSeasonNumber: Optional[int] = None


@dataclass(frozen=True)
class Image(Base):
    """Image metadata.

    Attribute of Series.
    """

    coverType: str
    url: str


@dataclass(frozen=True)
class Tag(Base):
    """User-applied metadata.

    Attribute of Series.
    """

    label: str
    id: int


@dataclass(frozen=True)
class Series(Base):
    """TV series metadata.

    Returned by /series, /series/lookup.

    Attribute of Episode, Download, ParseResult.
    """

    tvdbId: int
    title: str
    cleanTitle: str
    monitored: bool
    seasonFolder: bool
    titleSlug: str
    tvRageId: Optional[int] = None
    runtime: Optional[int] = None
    status: Optional[str] = None
    qualityProfileId: Optional[int] = None
    images: Tuple[Image, ...] = ()
    seriesType: Optional[str] = None
    useSceneNumbering: Optional[bool] = None
    year: Optional[int] = None
    seasons: Tuple[Season, ...] = ()
    id: Optional[int] = None
    airTime: Optional[time] = None
    overview: Optional[str] = None
    imdbId: Optional[str] = None
    network: Optional[str] = None
    qualityProfile: Optional[QualityProfile] = None
    sortTitle: Optional[str] = None
    seasonCount: Optional[int] = None
    profileId: Optional[int] = None
    tvMazeId: Optional[int] = None
    certification: Optional[str] = None
    genres: Tuple[str, ...] = ()
    tags: Tuple[int, ...] = ()
    added: Optional[datetime] = None
    ratings: Optional[Rating] = None
    alternateTitles: Tuple[AlternateTitle, ...] = ()
    totalEpisodeCount: Optional[int] = None
    episodeCount: Optional[int] = None
    episodeFileCount: Optional[int] = None
    sizeOnDisk: Optional[int] = None
    firstAired: Optional[datetime] = None
    previousAiring: Optional[datetime] = None
    nextAiring: Optional[datetime] = None
    remotePoster: Optional[str] = None
    lastInfoSync: Optional[datetime] = None
    path: Optional[str] = None
