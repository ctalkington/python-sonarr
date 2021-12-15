"""Tests for Sonarr Models."""
import json
from datetime import datetime, timezone

import pytest

import arr.models
from arr import ArrError
from tests import load_fixture

INFO = json.loads(load_fixture("arr/system-status.json"))
COMMAND = json.loads(load_fixture("arr/command.json"))
DISKSPACE = json.loads(load_fixture("arr/diskspace.json"))

APPLICATION = {"info": INFO, "diskspace": DISKSPACE}


def test_application() -> None:
    """Test the Application model."""
    app = arr.models.Application(APPLICATION)

    assert app

    assert app.info
    assert isinstance(app.info, arr.models.Info)

    assert app.disks
    assert len(app.disks) == 1
    assert isinstance(app.disks[0], arr.models.Disk)


def test_application_no_data() -> None:
    """Test the Device model."""
    with pytest.raises(ArrError):
        arr.models.Application({})


def test_dt_str_to_dt() -> None:
    """Test the dt_str_to_dt method."""
    dt = arr.models.dt_str_to_dt("2018-05-14T19:02:13.101496Z")
    assert dt == datetime(2018, 5, 14, 19, 2, 13, 100000, tzinfo=timezone.utc)


def test_dt_str_to_dt_long_microseconds() -> None:
    """Test the dt_str_to_dt method with long microseconds."""
    dt = arr.models.dt_str_to_dt("2018-05-14T19:02:13.1014986Z")
    assert dt == datetime(2018, 5, 14, 19, 2, 13, 100000, tzinfo=timezone.utc)


def test_info() -> None:
    """Test the Info model."""
    info = arr.models.Info.from_dict(INFO)

    assert info
    assert info.app_name == "Sonarr"
    assert info.version == "2.0.0.1121"


def test_command_item() -> None:
    """Test the CommandItem model."""
    item = arr.models.CommandItem.from_dict(COMMAND[0])

    assert item
    assert item.name == "RefreshSeries"
    assert item.message == "Not Provided"
    assert item.state == "started"
    assert item.priority == "normal"
    assert item.trigger == "manual"
    assert item.started == datetime(2020, 4, 6, 16, 54, 6, 420000, tzinfo=timezone.utc)
    assert item.queued == datetime(2020, 4, 6, 16, 54, 6, 410000, tzinfo=timezone.utc)
    assert item.changed == datetime(2020, 4, 6, 16, 54, 6, 420000, tzinfo=timezone.utc)

    item = arr.models.CommandItem.from_dict(COMMAND[1])

    assert item
    assert item.name == "RefreshSeries"
    assert item.message == "Not Provided"
    assert item.state == "started"
    assert item.priority == "unknown"
    assert item.trigger == "unknown"
    assert item.started == datetime(2020, 4, 6, 16, 57, 51, 400000, tzinfo=timezone.utc)
    assert item.queued == datetime(2020, 4, 6, 16, 57, 51, 400000, tzinfo=timezone.utc)
    assert item.changed == datetime(2020, 4, 6, 16, 57, 51, 410000, tzinfo=timezone.utc)


def test_disk() -> None:
    """Test the Disk model."""
    disk = arr.models.Disk.from_dict(DISKSPACE[0])

    assert disk
    assert disk.path == "C:\\"
    assert disk.label == ""
    assert disk.free == 282500067328
    assert disk.total == 499738734592
