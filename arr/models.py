from dataclasses import dataclass
from datetime import datetime
from typing import List

from arr import ArrError


def dt_str_to_dt(dt_str: str) -> datetime:
    """Convert ISO-8601 datetime string to datetime object."""
    utc = False

    if "Z" in dt_str:
        utc = True
        dt_str = dt_str[:-1]

    if "." in dt_str:
        # Python doesn't support long microsecond values
        ts_bits = dt_str.split(".", 1)
        dt_str = "{}.{}".format(ts_bits[0], ts_bits[1][:2])
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
    else:
        fmt = "%Y-%m-%dT%H:%M:%S"

    if utc:
        dt_str += "Z"
        fmt += "%z"

    return datetime.strptime(dt_str, fmt)


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
            started = dt_str_to_dt(started)

        if queued is not None:
            queued = dt_str_to_dt(queued)

        changed = data.get("stateChangeTime", None)
        if changed is not None:
            changed = dt_str_to_dt(changed)

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
    protocol: str
    size_remaining: int
    size: int
    status: str
    eta: datetime
    time_remaining: str

    @staticmethod
    def from_dict(data: dict):
        """Return QueueItem object from Arr API response."""
        eta = data.get("estimatedCompletionTime", None)
        if eta is not None:
            eta = dt_str_to_dt(eta)

        return QueueItem(
            queue_id=data.get("id", 0),
            download_id=data.get("downloadId", ""),
            download_status=data.get("trackedDownloadStatus", "Unknown"),
            title=data.get("title", "Unknown"),
            protocol=data.get("protocol", "unknown"),
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
        if any(k not in data for k in ["info"]):
            raise ArrError("Sonarr data is incomplete, cannot construct object")
        self.update_from_dict(data)

    def update_from_dict(self, data: dict) -> "Application":
        """Return Application object from Sonarr API response."""
        if "info" in data and data["info"]:
            self.info = Info.from_dict(data["info"])

        if "diskspace" in data and data["diskspace"]:
            disks = [Disk.from_dict(disk) for disk in data["diskspace"]]
            self.disks = disks

        return self


@dataclass(frozen=True)
class WantedResults:
    """Object holding wanted item results from Arr."""

    page: int
    per_page: int
    total: int
    sort_key: str
    sort_dir: str

    @staticmethod
    def from_dict(data: dict):
        """Return WantedResults object from Arr API response."""

        return WantedResults(
            page=data.get("page", 0),
            per_page=data.get("pageSize", 0),
            total=data.get("totalRecords", 0),
            sort_key=data.get("sortKey", ""),
            sort_dir=data.get("sortDirection", ""),
        )
