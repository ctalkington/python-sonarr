"""Tests for Sonarr Models."""
import json
import pytest
from sonarr import SonarrError
import sonarr.models as models

INFO = json.loads(load_fixture("system-status.json"))
DISKSPACE = json.loads(load_fixture("diskspace.json"))
APPLICATION = {"info": INFO, "diskspace": DISKSPACE}

def test_application() -> None:
    """Test the Application model."""
    app = models.Application(APPLICATION)

    assert app

    assert app.info
    assert isinstance(app.info, models.Info)

    assert app.disks
    assert len(device.disks) == 1
    assert isinstance(app.disks.locations[0], models.Disk)


def test_application_no_data() -> None:
    """Test the Device model."""
    with pytest.raises(SonarrError):
        models.Application({})


def test_info() -> None:
    """Test the Info model."""
    info = models.Info.from_dict(INFO)

    assert info
    assert info.brand == "Sonarr"
    assert info.version == "2.0.0.1121"


def test_disk() -> None:
    """Test the Disk model."""
    disk = models.Disk.from_dict(DISKSPACE[0])

    assert disk
    assert disk.path == "C:\\"
    assert disk.label == ""
    assert disk.free == 282500067328
    assert disk.total == 499738734592
