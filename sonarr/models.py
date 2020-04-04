"""Models for DirecTV."""

from dataclasses import dataclass
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
            label=data.get("label"),
            path=data.get("path"),
            free=data.get("freeSpace", 0),
            total=data.get("totalSpace", 0),
        )


@dataclass(frozen=True)
class Info:
    """Object holding information from Sonarr."""

    brand: str
    version: str

    @staticmethod
    def from_dict(data: dict):
        """Return Info object from Sonarr API response."""
        return Info(
            brand="Sonarr",
            version=data.get("version", "Unknown"),
        )


class Application:
    """Object holding all information of the Sonarr Application."""

    info: Info
    disks: List[Disk] = []

    def __init__(self, data: dict):
        """Initialize an empty Sonarr application class."""
        # Check if all elements are in the passed dict, else raise an Error
        if any(k not in data for k in ["info", "diskspace"]):
            raise SonarrError(
                "Sonarr data is incomplete, cannot construct object"
            )
        self.update_from_dict(data)

    def update_from_dict(self, data: dict) -> "Application":
        """Return Application object from Sonarr API response."""
        if "info" in data and data["info"]:
            self.info = Info.from_dict(data["info"])

        if "diskspace" in data and data["diskspace"]:
            disks = [Disk.from_dict(disk) for disk in data["diskspace"]]
            self.disks = disks

        return self
