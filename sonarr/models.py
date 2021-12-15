"""Models for Sonarr."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from arr.models import dt_str_to_dt, QueueItem as ArrQueueItem, WantedResults as ArrWantedResults


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
    poster: Optional[str]
    monitored: bool
    added: datetime
    synced: datetime

    @staticmethod
    def from_dict(data: dict):
        """Return Series object from Sonarr API response."""
        premiere = data.get("firstAired", None)
        if premiere is not None:
            premiere = dt_str_to_dt(premiere)

        added = data.get("added", None)
        if added is not None:
            added = dt_str_to_dt(added)

        synced = data.get("lastInfoSync", None)
        if synced is not None:
            synced = dt_str_to_dt(synced)

        poster = None
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
    airdate: str
    airs: datetime
    downloaded: bool
    downloading: bool
    series: Series

    @staticmethod
    def from_dict(data: dict):
        """Return Episode object from Sonarr API response."""
        airs = data.get("airDateUtc", None)
        if airs is not None:
            airs = dt_str_to_dt(airs)

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
            airdate=data.get("airDate", ""),
            airs=airs,
            downloaded=data.get("hasFile", False),
            downloading=data.get("downloading", False),
            series=Series.from_dict(data.get("series", {})),
        )


@dataclass(frozen=True)
class QueueItem(ArrQueueItem):
    """Object holding queue item information from Sonarr."""

    episode: Episode

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Sonarr API response."""
        arr_queue = ArrQueueItem.from_dict(data)

        episode_data = data.get("episode", {})
        episode_data["series"] = data.get("series", {})

        episode = Episode.from_dict(episode_data)

        return QueueItem(
            queue_id=arr_queue.queue_id,
            download_id=arr_queue.download_id,
            download_status=arr_queue.download_status,
            title=arr_queue.title,
            episode=episode,
            protocol=arr_queue.protocol,
            size=arr_queue.size,
            size_remaining=arr_queue.size_remaining,
            status=arr_queue.status,
            eta=arr_queue.eta,
            time_remaining=arr_queue.time_remaining,
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
class WantedResults(ArrWantedResults):
    """Object holding wanted episode results from Sonarr."""

    episodes: List[Episode]

    @staticmethod
    def from_dict(data: dict):
        """Return WantedResults object from Sonarr API response."""
        arr_wanted = ArrWantedResults.from_dict(data)

        episodes = [Episode.from_dict(episode) for episode in data.get("records", [])]

        return WantedResults(
            page=arr_wanted.page,
            per_page=arr_wanted.per_page,
            total=arr_wanted.total,
            sort_key=arr_wanted.sort_key,
            sort_dir=arr_wanted.sort_dir,
            episodes=episodes,
        )
