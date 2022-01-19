"""Asynchronous Python client for Radarr."""
from datetime import timedelta, date
from typing import List

from aiohttp.client import ClientSession

from arr.client import Client
from .models import (
    Movie, QueueItem,
)


class Radarr(Client):
    """Main class for Python API."""

    def __init__(
            self,
            host: str,
            api_key: str,
            base_path: str = "/api/v3/",
            port: int = 7878,
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

    async def calendar(self, start: str = None, end: str = None) -> List[Movie]:
        """Get upcoming movies.

        If start/end are not supplied, movies airing
        this week will be returned.
        """
        dt = date.today()
        if start is None:
            start = dt - timedelta(days=dt.weekday())

        if end is None:
            end = start + timedelta(days=6)

        results = await super().calendar(start, end)

        return [Movie.from_dict(result) for result in results]

    async def queue(self) -> List[QueueItem]:
        """Get currently downloading info."""
        results = await self._request("queue")

        return [QueueItem.from_dict(result) for result in results['records']]

    async def movies(self) -> List[Movie]:
        """Return all movies."""
        results = await self._request("movie")

        return [Movie.from_dict(result) for result in results]

    async def __aenter__(self) -> "Radarr":
        """Async enter."""
        return self
