"""Tests for Sonarr Models."""
import json
from datetime import datetime, timezone

import pytest
import sonarr.models as models
from sonarr import SonarrError

from . import load_fixture

INFO = json.loads(load_fixture("system-status.json"))
CALENDAR = json.loads(load_fixture("calendar.json"))
DISKSPACE = json.loads(load_fixture("diskspace.json"))
APPLICATION = {"info": INFO, "diskspace": DISKSPACE}


def test_application() -> None:
    """Test the Application model."""
    app = models.Application(APPLICATION)

    assert app

    assert app.info
    assert isinstance(app.info, models.Info)

    assert app.disks
    assert len(app.disks) == 1
    assert isinstance(app.disks[0], models.Disk)


def test_application_no_data() -> None:
    """Test the Device model."""
    with pytest.raises(SonarrError):
        models.Application({})


def test_info() -> None:
    """Test the Info model."""
    info = models.Info.from_dict(INFO)

    assert info
    assert info.app_name == "Sonarr"
    assert info.version == "2.0.0.1121"


def test_episode() -> None:
    """Test the Episode model."""
    episode = models.Episode.from_dict(CALENDAR[0])

    overview = """To compete with fellow \"restaurateur,\" Jimmy Pesto,
and his blowout Super Bowl event, Bob is determined to create a
Bob’s Burgers commercial to air during the \"big game.\"
In an effort to outshine Pesto, the Belchers recruit Randy
a documentarian, to assist with the filmmaking and hire on
former pro football star Connie Frye to be the celebrity endorser."""

    assert episode
    assert episode.tvdb_id == 0
    assert episode.episode_id == 14402
    assert episode.episode_number == 11
    assert episode.season_number == 4
    assert isinstance(episode.series, models.Series)
    assert episode.title == "Easy Com-mercial, Easy Go-mercial"
    assert episode.overview == overview.replace("\n", " ")
    assert episode.airs == datetime(2010, 7, 5, 15, 0, 8, tzinfo=timezone.utc)


def test_disk() -> None:
    """Test the Disk model."""
    disk = models.Disk.from_dict(DISKSPACE[0])

    assert disk
    assert disk.path == "C:\\"
    assert disk.label == ""
    assert disk.free == 282500067328
    assert disk.total == 499738734592


def test_series() -> None:
    """Test the Series model."""
    series = models.Series.from_dict(CALENDAR[0]["series"])

    overview = """Bob's Burgers follows a third-generation restaurateur,
Bob, as he runs Bob's Burgers with the help of his wife and their three
kids. Bob and his quirky family have big ideas about burgers, but fall
short on service and sophistication. Despite the greasy counters,
lousy location and a dearth of customers, Bob and his family are
determined to make Bob's Burgers \"grand re-re-re-opening\" a success."""

    assert series
    assert series.tvdb_id == 194031
    assert series.series_id == 66
    assert series.status == "continuing"
    assert series.slug == "bobs-burgers"
    assert series.title == "Bob's Burgers"
    assert series.overview == overview.replace("\n", " ")
    assert series.network == "FOX"
    assert series.runtime == 20
    assert series.timeslot == "5:30pm"
    assert series.premieres == datetime(2010, 7, 5, 15, 0, 8, tzinfo=timezone.utc)
