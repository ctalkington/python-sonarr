"""Tests for sonarr.models.system."""
import json
from datetime import datetime, timezone

import sonarr.models as models

from . import load_fixture

DISKSPACE = json.loads(load_fixture("diskspace.json"))
ROOTFOLDER = json.loads(load_fixture("rootfolder.json"))
SYSTEMSTATUS = json.loads(load_fixture("system-status.json"))
SYSTEMBACKUP = json.loads(load_fixture("system-backup.json"))
UTC = timezone.utc


def test_disk_space() -> None:
    """Test the DiskSpace model."""
    diskspace = models.DiskSpace.from_dict(DISKSPACE[0])
    assert diskspace.path == "C:\\"
    assert diskspace.label == ""
    assert diskspace.freeSpace == 282500067328
    assert diskspace.totalSpace == 499738734592


def test_unmapped_folder() -> None:
    """Test the UnmappedFolder model."""
    pass  # FIXME - need data


def test_root_folder() -> None:
    """Test the DiskSpace model."""
    rootfolder = models.RootFolder.from_dict(ROOTFOLDER[0])
    assert rootfolder.path == "C:\\Downloads\\TV"
    assert rootfolder.freeSpace == 282500063232
    assert rootfolder.unmappedFolders == ()
    assert rootfolder.id == 1


def test_system_status() -> None:
    """Test the SystemStatus model."""
    status = models.SystemStatus.from_dict(SYSTEMSTATUS)

    assert status.version == "2.0.0.1121"

    # "buildTime": "2014-02-08T20:49:36.5560392Z"
    # Round fractional seconds to microseconds
    assert status.buildTime == datetime(2014, 2, 8, 20, 49, 36, 556039, tzinfo=UTC)
    assert status.isDebug is False
    assert status.isProduction is True
    assert status.isAdmin is True
    assert status.isUserInteractive is False
    assert status.startupPath == "C:\\ProgramData\\NzbDrone\\bin"
    assert status.appData == "C:\\ProgramData\\NzbDrone"
    assert status.osVersion == "6.2.9200.0"
    assert status.isMono is False
    assert status.isLinux is False
    assert status.isWindows is True
    assert status.branch == "develop"
    assert status.authentication is False
    assert status.startOfWeek == 0
    assert status.urlBase == ""


def test_system_backup() -> None:
    """Test the SystemBackup model."""
    backup = models.SystemBackup.from_dict(SYSTEMBACKUP[0])
    assert backup.name == "nzbdrone_backup_2017.08.17_22.00.00.zip"
    assert backup.path == "/backup/update/nzbdrone_backup_2017.08.17_22.00.00.zip"
    assert backup.type == "update"
    assert backup.time == datetime(2017, 8, 18, 5, 00, 37, tzinfo=UTC)
    assert backup.id == 1207435784
