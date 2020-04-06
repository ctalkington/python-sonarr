"""Models for Sonarr."""

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
class Season:
    """Object holding season information from Sonarr."""

    number: int
    monitored: bool
    downloaded: int = 0
    episodes: int = 0
    total_episodes: int = 0
    progress: int = 0
    diskspace: int = 0

    @staticmethod
    def from_dict(data: dict):
        """Return Season object from Sonarr API response."""
        stats = data.get("statistics", {})

        return Season(
            number=data.get("seasonNumber", 0),
            monitored=data.get("monitored", False),
            downloaded=stats.get("episodeFileCount", 0),
            episodes=stats.get("episodeCount", 0),
            total_episodes=stats.get("totalEpisodeCount", 0),
            progress=stats.get("percentOfEpisodes", 0),
            diskspace=stats.get("sizeOnDisk", 0),
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
    seasons: int
    overview: str
    certification: str
    genres: List[str]
    network: str
    runtime: int
    timeslot: str
    year: int
    premiere: datetime
    path: str
    poster: str
    monitored: bool
    added: datetime
    synced: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return Series object from Sonarr API response."""
        premiere = data.get("firstAired", None)
        if premiere is not None:
            premiere = datetime.strptime(premiere, "%Y-%m-%dT%H:%M:%S%z")

        added = data.get("added", None)
        if added is not None:
            added = datetime.strptime(added, "%Y-%m-%dT%H:%M:%S.%f%z")

        synced = data.get("lastInfoSync", None)
        if synced is not None:
            synced = datetime.strptime(synced, "%Y-%m-%dT%H:%M:%S.%f%z")

        for image in data.get("images", []):
            if "poster" not in image["coverType"]:
                continue

            if "remoteUrl" in image:
                poster = image["remoteUrl"]
            else:
                poster = image["url"]

        return Series(
            tvdb_id=data.get("tvdbId", 0),
            series_id=data.get("id", 0),
            series_type=data.get("seriesType", "unknown"),
            slug=data.get("titleSlug", ""),
            status=data.get("status", "unknown"),
            title=data.get("title", ""),
            seasons=data.get("seasonCount", 0),
            overview=data.get("overview", ""),
            certification=data.get("certification", "None"),
            genres=data.get("genres", []),
            network=data.get("network", "Unknown"),
            runtime=data.get("runtime", 0),
            timeslot=data.get("airTime", ""),
            year=data.get("year", 0),
            premiere=premiere,
            path=data.get("path", ""),
            poster=poster,
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
    identifier: str
    title: str
    overview: str
    airs: datetime
    downloaded: bool
    downloading: bool
    series: Series

    @staticmethod
    def from_dict(data: dict):
        """Return Episode object from Sonarr API response."""
        airs = data.get("airDateUtc", None)
        if airs is not None:
            airs = datetime.strptime(airs, "%Y-%m-%dT%H:%M:%S%z")

        episode_number = data.get("episodeNumber", 0)
        season_number = data.get("seasonNumber", 0)
        identifier = f"S{season_number:02d}E{episode_number:02d}"

        return Episode(
            tvdb_id=data.get("tvDbEpisodeId", 0),
            episode_id=data.get("id", 0),
            episode_number=episode_number,
            season_number=season_number,
            identifier=identifier,
            title=data.get("title", ""),
            overview=data.get("overview", ""),
            airs=airs,
            downloaded=data.get("hasFile", False),
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
class CommandItem:
    """Object holding command item information from Sonarr."""

    command_id: int
    name: int
    state: str
    queued: datetime
    started: datetime
    changed: datetime
    priority: str = "unknown"
    trigger: str = "unknown"
    message: str = "Not Provided"
    send_to_client: bool = False

    @staticmethod
    def from_dict(data: dict):
        """Return CommandItem object from Sonarr API response."""
        if "started" in data:
            started = data.get("started", None)
        else:
            started = data.get("startedOn", None)

        if "queued" in data:
            queued = data.get("queued", None)
        else:
            queued = started

        if started is not None:
            started = datetime.strptime(started, "%Y-%m-%dT%H:%M:%S.%f%z")

        if queued is not None:
            queued = datetime.strptime(queued, "%Y-%m-%dT%H:%M:%S.%f%z")

        changed = data.get("stateChangeTime", None)
        if changed is not None:
            changed = datetime.strptime(changed, "%Y-%m-%dT%H:%M:%S.%f%z")

        return CommandItem(
            command_id=data.get("id", 0),
            name=data.get("name", "Unknown"),
            state=data.get("state", "unknown"),
            priority=data.get("priority", "unknown"),
            trigger=data.get("trigger", "unknown"),
            message=data.get("message", "Not Provided"),
            send_to_client=data.get("sendUpdatesToClient", False),
            queued=queued,
            started=started,
            changed=changed,
        )


@dataclass(frozen=True)
class QueueItem:
    """Object holding queue item information from Sonarr."""

    queue_id: int
    download_id: str
    download_status: str
    title: str
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
            download_status=data.get("trackedDownloadStatus", "Unknown"),
            title=data.get("title", "Unknown"),
            episode=episode,
            protocol=data.get("protocol", "unknown"),
            size=data.get("size", 0),
            size_remaining=data.get("sizeleft", 0),
            status=data.get("status", "Unknown"),
            eta=eta,
            time_remaining=data.get("timeleft", "00:00:00"),
        )


@dataclass(frozen=True)
class SeriesItem:
    """Object holding series item information from Sonarr."""

    series: Series
    seasons: List[Season]
    downloaded: int
    episodes: int
    total_episodes: int
    diskspace: int

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Sonarr API response."""
        seasons = [Season.from_dict(season) for season in data.get("seasons", [])]

        return SeriesItem(
            series=Series.from_dict(data),
            seasons=seasons,
            downloaded=data.get("episodeFileCount", 0),
            episodes=data.get("episodeCount", 0),
            total_episodes=data.get("totalEpisodeCount", 0),
            diskspace=data.get("sizeOnDisk", 0),
        )


@dataclass(frozen=True)
class WantedResults:
    """Object holding wanted episode results from Sonarr."""

    page: int
    per_page: int
    total: int
    sort_key: str
    sort_dir: str
    episodes: List[Episode]

    @staticmethod
    def from_dict(data: dict):
        """Return WantedResults object from Sonarr API response."""
        episodes = [Episode.from_dict(episode) for episode in data.get("records", [])]

        return WantedResults(
            page=data.get("page", 0),
            per_page=data.get("pageSize", 0),
            total=data.get("totalRecords", 0),
            sort_key=data.get("sortKey", ""),
            sort_dir=data.get("sortDirection", ""),
            episodes=episodes,
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
