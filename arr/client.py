"""Asynchronous Python client for Sonarr."""
import asyncio
import json
from socket import gaierror as SocketGIAError
from typing import Any, Mapping, Optional, List

import aiohttp
import async_timeout
from yarl import URL

from arr.__version__ import __version__
from arr.exceptions import (
    ArrAccessRestricted,
    ArrConnectionError,
    ArrError,
    ArrResourceNotFound,
)
from arr.models import Application, CommandItem, QueueItem, WantedResults


class Client:
    """Main class for handling connections with Sonarr API."""

    _application: Optional[Application] = None

    def __init__(
        self,
        host: str,
        api_key: str,
        base_path: str = "/api/",
        port: int = 8080,
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
            self.user_agent = f"PythonArr/{__version__}"

        if self.base_path[-1] != "/":
            self.base_path += "/"

    async def _request(
        self,
        uri: str = "",
        method: str = "GET",
        data: Optional[Any] = None,
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
                    data=data,
                    params=params,
                    headers=headers,
                    ssl=self.verify_ssl,
                )
        except asyncio.TimeoutError as exception:
            raise ArrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        except (aiohttp.ClientError, SocketGIAError) as exception:
            raise ArrConnectionError(
                "Error occurred while communicating with API"
            ) from exception

        if response.status == 403:
            raise ArrAccessRestricted(
                "Access restricted. Please ensure valid API Key is provided", {}
            )

        if response.status == 404:
            raise ArrResourceNotFound("Resource not found")

        content_type = response.headers.get("Content-Type", "")

        if (response.status // 100) in [4, 5]:
            content = await response.read()
            response.close()

            if content_type == "application/json":
                raise ArrError(
                    f"HTTP {response.status}", json.loads(content.decode("utf8"))
                )

            raise ArrError(
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

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "Client":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()

    async def update(self, full_update: bool = False) -> Application:
        """Get all information about the application in a single call."""
        if self._application is None or full_update:
            status = await self._request("system/status")
            if status is None:
                raise ArrError("{} returned an empty API status response".format(self.__class__.__name__))

            diskspace = await self._request("diskspace")

            self._application = Application({"info": status, "diskspace": diskspace})
            return self._application

        diskspace = await self._request("diskspace")
        self._application.update_from_dict({"diskspace": diskspace})
        return self._application

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

    @property
    def app(self) -> Optional[Application]:
        """Return the cached Application object."""
        return self._application

