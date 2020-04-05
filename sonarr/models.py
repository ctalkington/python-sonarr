"""Models for DirecTV."""

from dataclasses import dataclass
from datetime import datetime
from typing import List

from .exceptions import SonarrError


@dataclass(frozen=True)
class Disk:
    """Object holding disk information from Sonarr."""

    label: str
    path: str
    free: int
    total: int

    @staticmethod
    def from_dict(data: dict):
        """Return Disk object from Sonarr API response."""
        return Disk(
            label=data.get("label", ""),
            path=data.get("path", ""),
            free=data.get("freeSpace", 0),
            total=data.get("totalSpace", 0),
        )


@dataclass(frozen=True)
class Series:
    """Object holding series information from Sonarr."""

    tvdb_id: int
    series_id: int
    series_type: str
    slug: str
    status: str
    title: str
    overview: str
    certification: str
    network: str
    runtime: int
    timeslot: str
    premieres: datetime
    path: str
    monitored: bool
    added: datetime
    synced: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return Series object from Sonarr API response."""
        premieres = data.get("firstAired", None)
        if premieres is not None:
            premieres = datetime.strptime(premieres, "%Y-%m-%dT%H:%M:%S%z")

        added = data.get("added", None)
        if added is not None:
            added = datetime.strptime(added, "%Y-%m-%dT%H:%M:%S.%f%z")

        synced = data.get("lastInfoSync", None)
        if synced is not None:
            synced = datetime.strptime(synced, "%Y-%m-%dT%H:%M:%S.%f%z")

        return Series(
            tvdb_id=data.get("tvdbId", 0),
            series_id=data.get("id", 0),
            series_type=data.get("seriesType", "unknown"),
            slug=data.get("titleSlug", ""),
            status=data.get("status", "unknown"),
            title=data.get("title", ""),
            overview=data.get("overview", ""),
            certification=data.get("certification", "None"),
            network=data.get("network", "Unknown"),
            runtime=data.get("runtime", 0),
            timeslot=data.get("airTime", ""),
            premieres=premieres,
            path=data.get("path", ""),
            added=added,
            synced=synced,
            monitored=data.get("monitored", False),
        )


@dataclass(frozen=True)
class Episode:
    """Object holding episode information from Sonarr."""

    tvdb_id: int
    episode_id: int
    episode_number: int
    season_number: int
    title: str
    overview: str
    airs: datetime
    downloading: bool
    series: Series

    @staticmethod
    def from_dict(data: dict):
        """Return Episode object from Sonarr API response."""
        airs = data.get("airDateUtc", None)
        if airs is not None:
            airs = datetime.strptime(airs, "%Y-%m-%dT%H:%M:%S%z")

        return Episode(
            tvdb_id=data.get("tvDbEpisodeId", 0),
            episode_id=data.get("id", 0),
            episode_number=data.get("episodeNumber", 0),
            season_number=data.get("seasonNumber", 0),
            title=data.get("title", ""),
            overview=data.get("overview", ""),
            airs=airs,
            downloading=data.get("downloading", False),
            series=Series.from_dict(data.get("series", {})),
        )


@dataclass(frozen=True)
class Info:
    """Object holding information from Sonarr."""

    app_name: str
    version: str

    @staticmethod
    def from_dict(data: dict):
        """Return Info object from Sonarr API response."""
        return Info(app_name="Sonarr", version=data.get("version", "Unknown"))

@dataclass(frozen=True)
class QueueItem:
    """Object holding queue item information from Sonarr."""

    queue_id: int
    download_id: str
    episode: Episode
    protocol: str
    size_remaining: int
    size: int
    status: str
    eta: datetime
    time_remaining: str

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Sonarr API response."""
        episode_data = data.get("episode", {})
        episode_data["series"] = data.get("series", {})
        
        episode = Episode.from_dict(episode_data)

        eta = data.get("estimatedCompletionTime", None)
        if eta is not None:
            eta = datetime.strptime(eta, "%Y-%m-%dT%H:%M:%S.%f%z")

        return QueueItem(
            queue_id=data.get("id", 0),
            download_id=data.get("downloadId", ""),
            episode=episode,
            protocol=data.get("protocol, "unknown"),
            size=data.get("size", 0),
            size_remaining=data.get("sizeleft", 0),
            status=data.get("status", "Unknown"),
            eta=eta,
            time_remaining=data.get("timeleft", "00:00:00"),
        )


class Application:
    """Object holding all information of the Sonarr Application."""

    info: Info
    disks: List[Disk] = []

    def __init__(self, data: dict):
        """Initialize an empty Sonarr application class."""
        # Check if all elements are in the passed dict, else raise an Error
        if any(k not in data for k in ["info", "diskspace"]):
            raise SonarrError("Sonarr data is incomplete, cannot construct object")
        self.update_from_dict(data)

    def update_from_dict(self, data: dict) -> "Application":
        """Return Application object from Sonarr API response."""
        if "info" in data and data["info"]:
            self.info = Info.from_dict(data["info"])

        if "diskspace" in data and data["diskspace"]:
            disks = [Disk.from_dict(disk) for disk in data["diskspace"]]
            self.disks = disks

        return self
