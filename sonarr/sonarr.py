"""Asynchronous Python client for Sonarr.

https://github.com/Sonarr/Sonarr/wiki/API
"""
import asyncio
import json
from socket import gaierror as SocketGIAError
from typing import Any, Tuple, Mapping, Optional, Sequence
from datetime import date

import aiohttp
import async_timeout
from yarl import URL

from .__version__ import __version__
from .exceptions import SonarrAccessRestricted, SonarrConnectionError, SonarrError
from .models import (
    SortKey,
    SortDirection,
    Protocol,
    CommandStatus,
    Episode,
    EpisodeFile,
    WantedMissing,
    History,
    QueueItem,
    Image,
    Tag,
    Series,
    DiskSpace,
    QualityRevision,
    ParseResult,
    QualityAllowedProfile,
    Release,
    RootFolder,
    Season,
    SystemStatus,
    SystemBackup,
)
from .models.base import encode_dict


BOOL2JSON = {True: "true", False: "false"}


class Sonarr:
    """Main class for handling connections with Sonarr API."""

    #  _application: Optional[Application] = None

    def __init__(
        self,
        host: str,
        api_key: str,
        base_path: str = "/api/",
        port: int = 8989,
        request_timeout: int = 8,
        session: aiohttp.client.ClientSession = None,
        tls: bool = False,
        verify_ssl: bool = True,
        user_agent: str = None,
    ) -> None:
        """Initialize connection with receiver."""
        self._session = session
        self._close_session = False

        self.api_key = api_key
        self.base_path = base_path
        self.host = host
        self.port = port
        self.request_timeout = request_timeout
        self.tls = tls
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"PythonSonarr/{__version__}"

        if self.base_path[-1] != "/":
            self.base_path += "/"

    async def _request(
        self,
        uri: str = "",
        method: str = "GET",
        body: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Handle a request to API."""
        scheme = "https" if self.tls else "http"

        url = URL.build(
            scheme=scheme, host=self.host, port=self.port, path=self.base_path
        ).join(URL(uri))

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "X-Api-Key": self.api_key,
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    params=params,
                    json=body,
                    headers=headers,
                    ssl=self.verify_ssl,
                )
        except asyncio.TimeoutError as exception:
            raise SonarrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        except (aiohttp.ClientError, SocketGIAError) as exception:
            raise SonarrConnectionError(
                "Error occurred while communicating with API"
            ) from exception

        if response.status == 403:
            raise SonarrAccessRestricted(
                "Access restricted. Please ensure valid API Key is provided", {}
            )

        content_type = response.headers.get("Content-Type", "")

        if (response.status // 100) in [4, 5]:
            content = await response.read()
            response.close()

            if content_type == "application/json":
                raise SonarrError(
                    f"HTTP {response.status}", json.loads(content.decode("utf8"))
                )

            raise SonarrError(
                f"HTTP {response.status}",
                {
                    "content-type": content_type,
                    "message": content.decode("utf8"),
                    "status-code": response.status,
                },
            )

        if "application/json" in content_type:
            data = await response.json()
            return data

        return await response.text()

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "Sonarr":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()

    #  https://github.com/Sonarr/Sonarr/wiki/Calendar
    async def get_calendar(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None
    ) -> Tuple[Episode, ...]:
        """Get upcoming episodes.

        If start/end are not supplied, episodes airing today and tomorrow
        will be returned.
        """
        params = {}

        if start is not None:
            params["start"] = start.isoformat()

        if end is not None:
            params["end"] = end.isoformat()

        results = await self._request("calendar", params=params)
        return tuple(Episode.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Command
    async def get_all_commands(self) -> Tuple[CommandStatus, ...]:
        """Query the status of all currently started commands."""
        results = await self._request("command")
        return tuple(CommandStatus.from_dict(result) for result in results)

    async def get_command(self, command_id: int) -> CommandStatus:
        """Query the status of a previously started command."""
        result = await self._request(f"command/{command_id}")
        return CommandStatus.from_dict(result)

    async def _post_command(self, name: str, **kwargs) -> CommandStatus:
        """POST a request to /api/command.

        All POST/PUT requests require all parameters to be JSON encoded in the
        body, unless otherwise noted.
        """
        body = {"name": name}
        body.update(kwargs)
        results = await self._request("command", method="POST", body=body)
        return CommandStatus.from_dict(results)

    async def refresh_all_series(self) -> CommandStatus:
        """Refresh all series information from trakt and rescan disk."""
        results = await self._post_command("RefreshSeries")
        return results

    async def refresh_series(self, seriesId: int) -> CommandStatus:
        """Refresh single series information from trakt and rescan disk."""
        results = await self._post_command("RefreshSeries", seriesId=seriesId)
        return results

    async def rescan_all_series(self) -> CommandStatus:
        """Refresh rescan disk for all series."""
        results = await self._post_command("RescanSeries")
        return results

    async def rescan_series(self, seriesId: int) -> CommandStatus:
        """Refresh rescan disk for a single series."""
        results = await self._post_command("RescanSeries", seriesId=seriesId)
        return results

    async def search_episodes(self, episodeIds: Sequence[int]) -> CommandStatus:
        """Search for one or more episodes."""
        results = await self._post_command("EpisodeSearch", episodeIds=list(episodeIds))
        return results

    async def search_season(self, seriesId: int, seasonNumber: int) -> CommandStatus:
        """Search for all episodes of a particular season."""
        results = await self._post_command(
            "SeasonSearch", seriesId=seriesId, seasonNumber=seasonNumber
        )
        return results

    async def search_series(self, seriesId: int) -> CommandStatus:
        """Search for all episodes in a series."""
        results = await self._post_command("SeriesSearch", seriesId=seriesId)
        return results

    #  async def downloaded_episodes_scan(self) -> CommandStatus:
    #      """Instruct Sonarr to scan and import the folder defined by the
    #      path variable set in the POSTed json body.
    #      """
    #      pass

    async def sync_rss(self) -> CommandStatus:
        """Instruct Sonarr to perform an RSS sync with all enabled indexers."""
        results = await self._post_command("RssSync")
        return results

    async def rename_files(self, files: Sequence[int]) -> CommandStatus:
        """Instruct Sonarr to rename the list of files provided."""
        results = await self._post_command("RenameFiles", files=list(files))
        return results

    async def rename_series(self, seriesIds: Sequence[int]) -> CommandStatus:
        """Instruct Sonarr to rename all files in the provided series."""
        results = await self._post_command("RenameSeries", seriesIds=list(seriesIds))
        return results

    async def backup(self) -> CommandStatus:
        """Instruct Sonarr to perform a backup of its database and config file
        (nzbdrone.db and config.xml).
        """
        results = await self._post_command("Backup")
        return results

    async def search_missing_episodes(self) -> CommandStatus:
        """Instruct Sonarr to perform a backlog search of missing episodes
        (Similar functionality to Sickbeard).
        """
        results = await self._post_command("missingEpisodeSearch")
        return results

    #  https://github.com/Sonarr/Sonarr/wiki/Diskspace
    async def get_diskspace(self) -> Tuple[DiskSpace, ...]:
        results = await self._request("diskspace")
        return tuple(DiskSpace.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Episode
    async def get_episodes(self, seriesId) -> Tuple[Episode, ...]:
        """Returns all episodes for the given series."""
        params = {"seriesId": seriesId}
        results = await self._request("episode", params=params)
        return tuple(Episode.from_dict(result) for result in results)

    async def get_episode(self, episodeId: int) -> Episode:
        """Returns the episode with the matching id."""
        result = await self._request(f"episode/{episodeId}")
        return Episode.from_dict(result)

    async def update_episode(self, episode: Episode) -> Episode:
        """Update the given episodes.
        Currently only monitored is changed, all other modifications are ignored.
        """
        body = episode.to_dict()
        result = await self._request("episode", method="PUT", body=body)
        return Episode.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/EpisodeFile
    async def get_episode_files(self, seriesId) -> Tuple[EpisodeFile, ...]:
        """Returns all episodes for the given series."""
        params = {"seriesId": seriesId}
        results = await self._request("episodefile", params=params)
        return tuple(EpisodeFile.from_dict(result) for result in results)

    async def get_episode_file(self, episodeFileId: int) -> EpisodeFile:
        """Returns the episode with the matching id."""
        result = await self._request(f"episodefile/{episodeFileId}")

        return EpisodeFile.from_dict(result)

    async def delete_episode_file(self, episodeFileId: int) -> bool:
        """Delete the given episode file."""
        result = await self._request(f"episodefile/{episodeFileId}", method="DELETE")
        return result == {}

    async def update_episode_file(
        self,
        episodeFileId: int,
        qualityRevision: QualityRevision
    ) -> EpisodeFile:
        """ Updates the quality of the episode file and returns the episode file.
        """
        body = qualityRevision.to_dict()
        result = await self._request(
            f"episodefile/{episodeFileId}", method="PUT", body=body
        )
        return EpisodeFile.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/History
    async def get_history(
        self,
        sortKey: SortKey = SortKey.DATE,
        page: int = 1,
        pageSize: int = 10,
        sortDir: SortDirection = SortDirection.ASCENDING,
        episodeId: Optional[int] = None,
    ) -> History:
        """Gets history (grabs/failures/completed).

        If provided, episodeId filters to a specific episode ID.
        """
        params = {
            "sortKey": sortKey.value,
            "page": page,
            "pageSize": pageSize,
            "sortDir": sortDir.value.replace("ending", ""),  # "asc"/"desc"
        }
        if episodeId is not None:
            params["episodeId"] = episodeId

        result = await self._request("history", params=params)
        return History.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/Images
    #  async def get_image(self) -> Image:
    #      """FIXME"""
    #      pass

    #  https://github.com/Sonarr/Sonarr/wiki/Wanted-Missing
    async def get_wanted_missing(
        self,
        sortKey: SortKey = SortKey.AIRDATE,
        page: int = 1,
        pageSize: int = 10,
        sortDir: SortDirection = SortDirection.DESCENDING,
    ) -> WantedMissing:
        """Get wanted missing episodes."""
        params = {
            "sortKey": sortKey.value,
            "page": str(page),
            "pageSize": str(pageSize),
            "sortDir": sortDir.value.replace("ending", ""),  # "asc"/"desc"
        }

        result = await self._request("wanted/missing", params=params)
        return WantedMissing.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/Queue
    async def get_queue(self) -> Tuple[QueueItem, ...]:
        """Get currently downloading info."""
        results = await self._request("queue")

        return tuple(QueueItem.from_dict(result) for result in results)

    async def delete_queue_item(self, queueItemId, blacklist=False) -> bool:
        """Deletes an item from the queue and download client.
        Optionally blacklist item after deletion.
        """
        params = {"id": queueItemId, "blacklist": BOOL2JSON[blacklist]}
        result = await self._request("queue", method="DELETE", params=params)
        return result == {}

    #  https://github.com/Sonarr/Sonarr/wiki/Parse
    async def parse_title(self, title: str) -> ParseResult:
        """Returns the result of parsing a title.

        Series and episodes will be returned only if the parsing matches to a
        specific series and one or more episodes.
        """
        params = {"title": title}
        result = await self._request("parse", params=params)
        return ParseResult.from_dict(result)

    async def parse_path(self, path: str) -> ParseResult:
        """Returns the result of parsing a path.

        Series and episodes will be returned only if the parsing matches to a
        specific series and one or more episodes.
        """
        params = {"path": path}
        result = await self._request("parse", params=params)
        return ParseResult.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/Profile
    async def get_profiles(self) -> Tuple[QualityAllowedProfile, ...]:
        """Gets all quality profiles."""
        results = await self._request("profile")
        return tuple(QualityAllowedProfile.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Release
    async def get_release(self, episodeId: int) -> Tuple[Release, ...]:
        """ """
        params = {"episodeId": episodeId}
        results = await self._request("release", params=params)
        return tuple(Release.from_dict(result) for result in results)

    async def add_release(self, guid: str, indexerId: int) -> Tuple[Release, ...]:
        """Adds a previously searched release to the download client,
        if the release is still in Sonarr's search cache (30 minute cache).
        If the release is not found in the cache Sonarr will return a 404.
        """
        body = {"guid": guid, "indexerId": indexerId}

        try:
            results = await self._request("release", method="POST", body=body)
        except SonarrError as err:
            if "404" in err.args[0]:
                msg = f"add_release(): {guid} not found"
                raise SonarrError(msg)
            else:
                raise

        return tuple(Release.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Release-Push
    async def push_release(
        self,
        title: str,
        downloadUrl: str,
        protocol: Protocol,
        publishDate: date
    ) -> Tuple[Release, ...]:
        """If the title is wanted, Sonarr will grab it."""
        body = encode_dict(
            {
                "title": title,
                "downloadUrl": downloadUrl,
                "protocol": protocol,
                "publishDate": publishDate,
            }
        )
        results = await self._request("release/push", method="POST", body=body)
        return tuple(Release.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Rootfolder
    async def get_rootfolders(self) -> Tuple[RootFolder, ...]:
        """ """
        results = await self._request("rootfolder")
        return tuple(RootFolder.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Series
    async def get_all_series(self) -> Tuple[Series, ...]:
        """Return all series."""
        results = await self._request("series")
        return tuple(Series.from_dict(result) for result in results)

    async def get_series(self, seriesId) -> Series:
        """Return the series with the matching ID
        or 404 if no matching series is found.
        """
        try:
            result = await self._request(f"series/{seriesId}")
        except SonarrError as err:
            if "404" in err.args[0]:
                msg = f"get_series(): {seriesId} not found"
                raise SonarrError(msg)
            else:
                raise

        return Series.from_dict(result)

    async def add_series(
        self,
        tvdbId: int,
        title: str,
        profileId: int,
        titleSlug: str,
        images: Tuple[Image, ...] = (),
        seasons: Tuple[Season, ...] = (),
        path: Optional[str] = None,
        rootFolderPath: Optional[str] = None,
        tvRageId: Optional[int] = None,
        seasonFolder: bool = True,
        monitored: bool = True,
        ignoreEpisodesWithFiles: bool = False,
        ignoreEpisodesWithoutFiles: bool = False,
        searchForMissingEpisodes: bool = False,
    ) -> Series:
        """Add a new series to your collection."""
        if (path or rootFolderPath) is None or (path and rootFolderPath):
            msg = "add_series(): must set exactly one of {path,rootFolderPath}"
            raise ValueError(msg)
        addOptions = {
            "ignoreEpisodesWithFiles": ignoreEpisodesWithFiles,
            "ignoreEpisodesWithoutFiles": ignoreEpisodesWithoutFiles,
            "searchForMissingEpisodes": searchForMissingEpisodes,
        }
        body = {
            "tvdbId": tvdbId,
            "title": title,
            "profileId": profileId,
            "titleSlug": titleSlug,
            "images": list(i.to_dict() for i in images),
            "seasons": list(s.to_dict() for s in seasons),
            "seasonFolder": seasonFolder,
            "monitored": monitored,
            "addOptions": addOptions,
        }

        if path is not None:
            body["path"] = path

        if rootFolderPath is not None:
            body["rootFolderPath"] = rootFolderPath

        if tvRageId is not None:
            body["tvRageId"] = tvRageId

        result = await self._request("series", method="POST", body=body)
        return Series.from_dict(result)

    async def update_series(self, series: Series) -> Series:
        """Update an existing series."""
        body = series.to_dict()
        result = await self._request("series", method="PUT", body=body)
        return Series.from_dict(result)

    async def delete_series(self, seriesId: int, deleteFiles: bool = False) -> bool:
        """Delete the series with the given ID."""
        params = {"id": seriesId, "deleteFiles": json.dumps(deleteFiles)}
        result = await self._request(f"series/{seriesId}", method="DELETE", params=params)
        return result == {}

    #  https://github.com/Sonarr/Sonarr/wiki/Series-Lookup
    async def lookup_series(self, term: str) -> Tuple[Series, ...]:
        """Searches for new shows on TheTVDB.com
        utilizing sonarr.tv's caching and augmentation proxy.
        """
        params = {"term": term}
        results = await self._request("series/lookup", params=params)
        return tuple(Series.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/System-Status
    async def get_system_status(self) -> SystemStatus:
        """Return system status."""
        result = await self._request("system/status")
        return SystemStatus.from_dict(result)

    #  https://github.com/Sonarr/Sonarr/wiki/System-Backup
    async def get_system_backups(self) -> Tuple[SystemBackup, ...]:
        """Return the list of available backups."""
        results = await self._request("system/backup")
        return tuple(SystemBackup.from_dict(result) for result in results)

    #  https://github.com/Sonarr/Sonarr/wiki/Tag
    async def get_tags(self) -> Tuple[Tag, ...]:
        """Return all tags."""
        results = await self._request("tag")
        return tuple(Tag.from_dict(result) for result in results)

    async def get_tag(self, tagId: int) -> Tag:
        """Return the tag with the matching ID
        or 404 if no matching tag is found.
        """
        try:
            result = await self._request(f"tag/{tagId}")
        except SonarrError as err:
            if "404" in err.args[0]:
                msg = f"get_tag(): {tagId} not found"
                raise SonarrError(msg)
            else:
                raise

        return Tag.from_dict(result)

    async def add_tag(self, label: str) -> Tag:
        """Add a new tag."""
        body = {"label": label}
        result = await self._request("tag", method="POST", body=body)
        return Tag.from_dict(result)

    async def update_tag(self, tagId: int, label: str) -> Tag:
        """Update an existing tag."""
        body = {"label": label, "id": tagId}
        result = await self._request("tag", method="PUT", body=body)
        return Tag.from_dict(result)

    async def delete_tag(self, tagId: int) -> bool:
        """Delete the series with the given ID"""
        result = await self._request(f"tag/{tagId}", method="DELETE")
        return result == {}
