"""
https://github.com/Sonarr/Sonarr/wiki/Diskspace
https://github.com/Sonarr/Sonarr/wiki/Rootfolder
https://github.com/Sonarr/Sonarr/wiki/System-Status
https://github.com/Sonarr/Sonarr/wiki/System-Backup
"""
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime

from .base import Base


@dataclass(frozen=True)
class DiskSpace(Base):
    """Disk space information as reported by Sonarr.

    Returned by /diskspace.
    """

    path: str
    label: str
    freeSpace: int
    totalSpace: int


@dataclass(frozen=True)
class UnmappedFolder(Base):
    """Attribute of RootFolder"""

    name: str
    path: str


@dataclass(frozen=True)
class RootFolder(Base):
    """Returned by /rootfolder."""

    path: str
    freeSpace: int
    unmappedFolders: Tuple[UnmappedFolder, ...]
    id: int
    totalSpace: Optional[int] = None


@dataclass(frozen=True)
class SystemStatus(Base):
    """Returned by /system/status."""

    version: str
    buildTime: datetime
    isDebug: bool
    isProduction: bool
    isAdmin: bool
    isUserInteractive: bool
    startupPath: str
    appData: str
    osVersion: str
    isMono: bool
    isLinux: bool
    isWindows: bool
    branch: str
    authentication: bool
    urlBase: str
    startOfWeek: Optional[int] = None
    osName: Optional[str] = None
    runtimeVersion: Optional[str] = None
    runtimeName: Optional[str] = None
    isMonoRuntime: Optional[bool] = None
    isOsx: Optional[bool] = None
    sqliteVersion: Optional[str] = None


@dataclass(frozen=True)
class SystemBackup(Base):
    """Returned by /system/backup."""

    name: str
    path: str
    type: str
    time: datetime
    id: int
