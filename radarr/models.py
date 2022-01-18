from dataclasses import dataclass
from typing import List

from arr.models import QueueItem as ArrQueueItem


@dataclass(frozen=True)
class QueueItem(ArrQueueItem):
    movie_id: int

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Radarr API response."""
        arr_queue = ArrQueueItem.from_dict(data)

        return QueueItem(
            queue_id=arr_queue.queue_id,
            download_id=arr_queue.download_id,
            download_status=arr_queue.download_status,
            title=arr_queue.title,
            movie_id=data.get('movieId'),
            protocol=arr_queue.protocol,
            size=arr_queue.size,
            size_remaining=arr_queue.size_remaining,
            status=arr_queue.status,
            eta=arr_queue.eta,
            time_remaining=arr_queue.time_remaining,
        )


@dataclass(frozen=True)
class Image:
    """Object holding image information from Radarr."""

    cover_type: str
    url: str
    remote_url: str

    @staticmethod
    def from_dict(data: dict):
        """Return Image object from Radarr API response."""

        return Image(
            cover_type=data.get("coverType", 'poster'),
            url=data.get("url", None),
            remote_url=data.get("remoteUrl", None),
        )


@dataclass(frozen=True)
class Rating:
    """Object holding rating information from Radarr."""

    votes: int
    value: int

    @staticmethod
    def from_dict(data: dict):
        """Return Image object from Radarr API response."""

        return Rating(
            votes=data.get("votes", 0),
            value=data.get("value", 0),
        )


@dataclass(frozen=True)
class Collection:
    """Object holding collection information from Radarr."""

    name: str
    tmdb_id: int
    images: List[Image]

    @staticmethod
    def from_dict(data: dict):
        """Return Image object from Radarr API response."""

        images = []

        for image in data.get('images', []):
            images.append(Image.from_dict(image))

        return Collection(
            name=data.get("name"),
            tmdb_id=data.get("tmdbId"),
            images=images,
        )


@dataclass(frozen=True)
class MovieFile:
    """Object holding movie file information from Radarr."""

    movie_id: int
    relative_path: str
    path: str
    size: int
    date_added: str
    indexer_flags: int
    quality_cutoff_not_met: bool
    release_group: str
    id: int

    @staticmethod
    def from_dict(data: dict):
        """Return Image object from Radarr API response."""

        return MovieFile(
            movie_id=data.get('movieId'),
            relative_path=data.get('relativePath'),
            path=data.get('path'),
            size=data.get('size'),
            date_added=data.get('dateAdded'),
            indexer_flags=data.get('indexerFlags'),
            quality_cutoff_not_met=data.get('qualityCutoffNotMet'),
            release_group=data.get('releaseGroup'),
            id=data.get('id'),
        )


@dataclass(frozen=True)
class Movie:
    """Object holding movie information from Radarr."""

    id: int
    title: str
    sort_title: str
    size_on_disk: int
    overview: str
    in_cinemas: str
    physical_release: str
    images: List[Image]
    website: str
    year: int
    has_file: bool
    youtube_trailer_id: str
    studio: str
    path: str
    root_folder_path: str
    quality_profile_id: int
    monitored: bool
    minimum_availability: str
    is_available: bool
    folder_name: str
    runtime: int
    clean_title: str
    imdb_id: str
    tmdb_id: int
    title_slug: str
    certification: str
    genres: List[str]
    tags: List[int]
    added: str
    ratings: Rating
    collection: Collection
    status: str
    movie_file: MovieFile

    @staticmethod
    def from_dict(data: dict):
        """Return Image object from Radarr API response."""

        images = []

        for image in data.get('images', []):
            images.append(Image.from_dict(image))

        rating = Rating.from_dict(data.get('ratings'))
        collection = Collection.from_dict(data.get('collection')) if data.get('collection', False) else None
        movie_file = MovieFile.from_dict(data.get('movieFile', [])) if data.get('movieFile', False) else None

        return Movie(
            id=data.get('id'),
            title=data.get('title'),
            sort_title=data.get('sortTitle'),
            size_on_disk=data.get('sizeOnDisk'),
            overview=data.get('overview'),
            in_cinemas=data.get('inCinemas'),
            physical_release=data.get('physicalRelease'),
            images=images,
            website=data.get('website'),
            year=data.get('year'),
            has_file=data.get('hasFile'),
            youtube_trailer_id=data.get('youTubeTrailerId'),
            studio=data.get('studio'),
            path=data.get('path'),
            root_folder_path=data.get('rootFolderPath'),
            quality_profile_id=data.get('qualityProfileId'),
            monitored=data.get('monitored'),
            minimum_availability=data.get('minimumAvailability'),
            is_available=data.get('isAvailable'),
            folder_name=data.get('folderName'),
            runtime=data.get('runtime'),
            clean_title=data.get('cleanTitle'),
            imdb_id=data.get('imdbId'),
            tmdb_id=data.get('tmdbId'),
            title_slug=data.get('titleSlug'),
            certification=data.get('certification'),
            genres=data.get('genres'),
            tags=data.get('tags'),
            added=data.get('added'),
            ratings=rating,
            collection=collection,
            status=data.get('status'),
            movie_file=movie_file,
        )
