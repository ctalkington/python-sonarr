"""Tests for Sonarr Models."""
import json
from datetime import datetime, timezone
from typing import List

import pytest
import sonarr.models as models
from sonarr import SonarrError

from . import load_fixture

INFO = json.loads(load_fixture("system-status.json"))
CALENDAR = json.loads(load_fixture("calendar.json"))
DISKSPACE = json.loads(load_fixture("diskspace.json"))
QUEUE = json.loads(load_fixture("queue.json"))
SERIES = json.loads(load_fixture("series.json"))

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
Bob's Burgers commercial to air during the \"big game.\"
In an effort to outshine Pesto, the Belchers recruit Randy,
a documentarian, to assist with the filmmaking and hire on
former pro football star Connie Frye to be the celebrity endorser."""

    assert episode
    assert episode.tvdb_id == 0
    assert episode.episode_id == 14402
    assert episode.episode_number == 11
    assert episode.season_number == 4
    assert episode.identifier == "S04E11"
    assert isinstance(episode.series, models.Series)
    assert episode.title == "Easy Com-mercial, Easy Go-mercial"
    assert episode.overview == overview.replace("\n", " ")
    assert episode.airs == datetime(2014, 1, 27, 1, 30, tzinfo=timezone.utc)
    assert not episode.downloaded
    assert not episode.downloading


def test_disk() -> None:
    """Test the Disk model."""
    disk = models.Disk.from_dict(DISKSPACE[0])

    assert disk
    assert disk.path == "C:\\"
    assert disk.label == ""
    assert disk.free == 282500067328
    assert disk.total == 499738734592


def test_queue_item() -> None:
    """Test the QueueItem model."""
    item = models.QueueItem.from_dict(QUEUE[0])

    assert item.queue_id == 1503378561
    assert item.download_id == "SABnzbd_nzo_Mq2f_b"
    assert item.download_status == "Ok"
    assert item.status == "Downloading"
    assert item.title == "The.Andy.Griffith.Show.S01E01.x264-GROUP"
    assert item.protocol == "usenet"
    assert item.size == 4472186820
    assert item.size_remaining == 0
    assert item.eta == datetime(2016, 2, 5, 22, 46, 52, 440104, tzinfo=timezone.utc)
    assert item.time_remaining == "00:00:00"

    assert item.episode
    assert isinstance(item.episode, models.Episode)


def test_season() -> None:
    """Test the Season model."""
    season = models.Season.from_dict(SERIES[0]["seasons"][1])

    assert season
    assert season.number == 1
    assert not season.monitored
    assert season.episodes == 0
    assert season.downloaded == 0
    assert season.total_episodes == 32
    assert season.progress == 0
    assert season.diskspace == 0


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
    assert series.monitored
    assert series.tvdb_id == 194031
    assert series.series_id == 66
    assert series.series_type == "standard"
    assert series.status == "continuing"
    assert series.seasons == 4
    assert series.slug == "bobs-burgers"
    assert series.title == "Bob's Burgers"
    assert series.overview == overview.replace("\n", " ")
    assert series.network == "FOX"
    assert series.runtime == 30
    assert series.timeslot == "17:30"
    assert series.year == 2011
    assert series.premiere == datetime(2011, 1, 10, 1, 30, tzinfo=timezone.utc)
    assert series.path == "T:\\Bob's Burgers"
    assert series.poster == "http://slurm.trakt.us/images/posters/1387.6-300.jpg"
    assert series.certification == "TV-14"
    assert series.genres == ["Animation", "Comedy"]
    assert series.added == datetime(
        2011, 1, 26, 19, 25, 55, 455594, tzinfo=timezone.utc
    )
    assert series.synced == datetime(
        2014, 1, 26, 19, 25, 55, 455594, tzinfo=timezone.utc
    )


def test_series_item() -> None:
    """Test the SeriesItem model."""
    item = models.SeriesItem.from_dict(SERIES[0])

    assert item
    assert item.episodes == 0
    assert item.downloaded == 0
    assert item.total_episodes == 253
    assert item.diskspace == 0

    assert item.series
    assert isinstance(item.series, models.Series)

    assert item.seasons
    assert isinstance(item.seasons, List)
    assert len(item.seasons) == 9

    assert item.seasons[4]
    assert isinstance(item.seasons[4], models.Season)
    assert item.seasons[4].episodes == 8
    assert item.seasons[4].downloaded == 8
    assert item.seasons[4].total_episodes == 32
    assert item.seasons[4].progress == 100
    assert item.seasons[4].diskspace == 8000000000
