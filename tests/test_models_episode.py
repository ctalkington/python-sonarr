"""Tests for sonarr.models.episode."""
import json
from datetime import datetime, date, timezone

import sonarr.models as models

from . import load_fixture

EPISODE = json.loads(load_fixture("episode.json"))
EPISODEFILE = json.loads(load_fixture("episodefile.json"))
HISTORY = json.loads(load_fixture("history.json"))
QUEUE = json.loads(load_fixture("queue.json"))
WANTED = json.loads(load_fixture("wanted-missing.json"))

UTC = timezone.utc


def test_episode() -> None:
    """Test the Episode model."""
    # Episode instance returned by /episode
    ep = models.Episode.from_dict(EPISODE[0])

    assert ep
    assert ep.seriesId == 1
    assert ep.episodeFileId == 0
    assert ep.seasonNumber == 1
    assert ep.episodeNumber == 1
    assert ep.title == "Mole Hunt"
    assert ep.airDate == date(2009, 9, 17)
    assert ep.airDateUtc == datetime(2009, 9, 18, 2, tzinfo=UTC)
    assert ep.overview == (
        "Archer is in trouble with his Mother and the Comptroller because his "
        "expense account is way out of proportion to his actual expenses. So "
        "he creates the idea that a Mole has breached ISIS and he needs to get"
        " into the mainframe to hunt him down (so he can cover his tracks!). "
        "All this leads to a surprising ending."
    )
    assert ep.hasFile is False
    assert ep.monitored is True
    assert ep.sceneEpisodeNumber == 0
    assert ep.sceneSeasonNumber == 0
    assert ep.tvDbEpisodeId == 0
    assert ep.absoluteEpisodeNumber == 1
    assert ep.id == 1
    assert ep.sceneAbsoluteEpisodeNumber is None
    assert ep.series is None
    assert ep.downloading is None
    assert ep.unverifiedSceneNumbering is None
    assert ep.lastSearchTime is None

    # Episode instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(WANTED)
    ep0, ep1 = want.records
    assert isinstance(ep0, models.Episode)
    assert isinstance(ep1, models.Episode)

    assert ep0.seriesId == 3
    assert ep0.episodeFileId == 0
    assert ep0.seasonNumber == 4
    assert ep0.episodeNumber == 11
    assert ep0.title == "Easy Com-mercial, Easy Go-mercial"
    assert ep0.airDate == date(2014, 1, 26)
    assert ep0.airDateUtc == datetime(2014, 1, 27, 1, 30, tzinfo=UTC)
    assert ep0.overview == (
        'To compete with fellow "restaurateur," Jimmy Pesto, and his blowout '
        "Super Bowl event, Bob is determined to create a Bob's Burgers "
        'commercial to air during the "big game." In an effort to outshine '
        "Pesto, the Belchers recruit Randy, a documentarian, to assist with "
        "the filmmaking and hire on former pro football star Connie Frye to "
        "be the celebrity endorser."
    )
    assert ep0.hasFile is False
    assert ep0.monitored is True
    assert ep0.sceneEpisodeNumber == 0
    assert ep0.sceneSeasonNumber == 0
    assert ep0.tvDbEpisodeId == 0
    assert isinstance(ep0.series, models.Series)  # Series tested in test_models_series
    assert ep0.downloading is False
    assert ep0.id == 14402

    assert ep1.seriesId == 17
    assert ep1.episodeFileId == 0
    assert ep1.seasonNumber == 1
    assert ep1.episodeNumber == 1
    assert ep1.title == "The New Housekeeper"
    assert ep1.airDate == date(1960, 10, 3)
    assert ep1.airDateUtc == datetime(1960, 10, 3, 1, tzinfo=UTC)
    assert ep1.overview == (
        "Sheriff Andy Taylor and his young son Opie are in need of a new "
        "housekeeper. Andy's Aunt Bee looks like the perfect candidate and "
        "moves in, but her presence causes friction with Opie."
    )
    assert ep1.hasFile is False
    assert ep1.monitored is True
    assert ep1.sceneEpisodeNumber == 0
    assert ep1.sceneSeasonNumber == 0
    assert ep1.tvDbEpisodeId == 0
    assert isinstance(ep1.series, models.Series)  # Series tested in test_models_series
    assert ep1.downloading is False
    assert ep1.id == 889

    # Episode instance returned by /calendar
    pass  # /calendar JSON response (Bob's Burgers S04E11) duplicates /wanted/missing

    # Episode instance returned by /history
    hist = models.History.from_dict(HISTORY)
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ep0 = dl0.episode

    assert ep0.seriesId == 60
    assert ep0.episodeFileId == 3464
    assert ep0.seasonNumber == 1
    assert ep0.episodeNumber == 11
    assert ep0.title == "Cease Forcing Enemy"
    assert ep0.airDate == date(2016, 2, 29)
    assert ep0.airDateUtc == datetime(2016, 3, 1, 1, tzinfo=UTC)
    assert ep0.overview == (
        "Jane reels from a series of massive revelations about her tattoos "
        "and grapples with whether to trust Oscar. Meanwhile, a tattoo leads "
        "the team to a shocking discovery in the Black Sea."
    )
    assert ep0.hasFile is True
    assert ep0.monitored is True
    assert ep0.absoluteEpisodeNumber == 11
    assert ep0.unverifiedSceneNumbering is False
    assert ep0.id == 5276

    ep1 = dl1.episode
    assert ep1.seriesId == 60
    assert ep1.episodeFileId == 3464
    assert ep1.seasonNumber == 1
    assert ep1.episodeNumber == 11
    assert ep1.title == "Cease Forcing Enemy"
    assert ep1.airDate == date(2016, 2, 29)
    assert ep1.airDateUtc == datetime(2016, 3, 1, 1, tzinfo=UTC)
    assert ep1.overview == (
        "Jane reels from a series of massive revelations about her tattoos "
        "and grapples with whether to trust Oscar. Meanwhile, a tattoo leads "
        "the team to a shocking discovery in the Black Sea."
    )
    assert ep1.hasFile is True
    assert ep1.monitored is True
    assert ep1.absoluteEpisodeNumber == 11
    assert ep1.unverifiedSceneNumbering is False
    assert ep1.id == 5276

    # instance returned by /parse
    pass  # FIXME - need data

    # instance returned by /queue
    item = models.QueueItem.from_dict(QUEUE[0])
    ep = item.episode
    assert ep.seriesId == 17
    assert ep.episodeFileId == 0
    assert ep.seasonNumber == 1
    assert ep.episodeNumber == 1
    assert ep.title == "The New Housekeeper"
    assert ep.airDate == date(1960, 10, 3)
    assert ep.airDateUtc == datetime(1960, 10, 3, 1, tzinfo=UTC)
    assert ep.overview == (
        "Sheriff Andy Taylor and his young son Opie are in need of a new "
        "housekeeper. Andy's Aunt Bee looks like the perfect candidate and "
        "moves in, but her presence causes friction with Opie."
    )
    assert ep.hasFile is False
    assert ep.monitored is False
    assert ep.absoluteEpisodeNumber == 1
    assert ep.unverifiedSceneNumbering is False
    assert ep.id == 889


def test_episode_file() -> None:
    """Test the EpisodeFile model."""
    ep = models.EpisodeFile.from_dict(EPISODEFILE[0])

    assert ep
    assert ep.seriesId == 1
    assert ep.seasonNumber == 1
    assert ep.path == (
        "C:\\Test\\Breaking Bad\\Season 01\\"
        "Breaking Bad - S01E01 - Pilot [Bluray 720p].mkv"
    )
    assert ep.size == 2183157756
    assert ep.dateAdded == datetime(2013, 5, 29, 10, 42, 5, 133530, tzinfo=UTC)
    assert ep.sceneName == ""
    assert ep.quality.quality.id == 1
    assert ep.quality.quality.name == "Bluray 720p"
    assert ep.quality.proper is False
    assert ep.id == 1


def test_wanted_missing() -> None:
    """Test the WantedMissing model."""
    want = models.WantedMissing.from_dict(WANTED)

    assert want
    assert want.page == 1
    assert want.pageSize == 10
    assert want.sortDirection == models.SortDirection.DESCENDING
    assert want.totalRecords == 2
    assert len(want.records) == 2
    ep0, ep1 = want.records
    #  Episode tested in test_episode()
    assert isinstance(ep0, models.Episode)
    assert isinstance(ep1, models.Episode)
