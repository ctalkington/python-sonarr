"""Asynchronous Python client for Sonarr."""
from typing import List, Optional

from aiohttp.client import ClientSession

from .client import Client
from .exceptions import SonarrError
from .models import (
    Application,
    CommandItem,
    Episode,
    QueueItem,
    SeriesItem,
    WantedResults,
)


class Sonarr(Client):
    """Main class for Python API."""

    _application: Optional[Application] = None

    def __init__(
        self,
        host: str,
        api_key: str,
        base_path: str = "/api/",
        port: int = 8989,
        request_timeout: int = 8,
        session: ClientSession = None,
        tls: bool = False,
        verify_ssl: bool = True,
        user_agent: str = None,
    ) -> None:
        """Initialize connection with Sonarr."""
        super().__init__(
            host=host,
            api_key=api_key,
            base_path=base_path,
            port=port,
            request_timeout=request_timeout,
            session=session,
            tls=tls,
            verify_ssl=verify_ssl,
            user_agent=user_agent,
        )

    @property
    def app(self) -> Optional[Application]:
        """Return the cached Application object."""
        return self._application

    async def update(self, full_update: bool = False) -> Application:
        """Get all information about the application in a single call."""
        if self._application is None or full_update:
            status = await self._request("system/status")
            if status is None:
                raise SonarrError("Sonarr returned an empty API status response")

            diskspace = await self._request("diskspace")

            self._application = Application({"info": status, "diskspace": diskspace})
            return self._application

        diskspace = await self._request("diskspace")
        self._application.update_from_dict({"diskspace": diskspace})
        return self._application

    async def calendar(self, start: str = None, end: str = None) -> List[Episode]:
        """Get upcoming episodes.

        If start/end are not supplied, episodes airing
        today and tomorrow will be returned.
        """
        params = {}

        if start is not None:
            params["start"] = str(start)

        if end is not None:
            params["end"] = str(end)

        results = await self._request("calendar", params=params)

        return [Episode.from_dict(result) for result in results]

    async def commands(self) -> List[CommandItem]:
        """Query the status of all currently started commands."""
        results = await self._request("command")

        return [CommandItem.from_dict(result) for result in results]

    async def command_status(self, command_id: int) -> CommandItem:
        """Query the status of a previously started command."""
        result = await self._request(f"command/{command_id}")

        return CommandItem.from_dict(result)

    async def queue(self) -> List[QueueItem]:
        """Get currently downloading info."""
        results = await self._request("queue")

        return [QueueItem.from_dict(result) for result in results]

    async def series(self) -> List[SeriesItem]:
        """Return all series."""
        results = await self._request("series")

        return [SeriesItem.from_dict(result) for result in results]

    async def wanted(
        self,
        sort_key: str = "airDateUtc",
        page: int = 1,
        page_size: int = 10,
        sort_dir: str = "desc",
    ) -> WantedResults:
        """Get wanted missing episodes."""
        params = {
            "sortKey": sort_key,
            "page": str(page),
            "pageSize": str(page_size),
            "sortDir": sort_dir,
        }

        results = await self._request("wanted/missing", params=params)

        return WantedResults.from_dict(results)

    async def __aenter__(self) -> "Sonarr":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()
