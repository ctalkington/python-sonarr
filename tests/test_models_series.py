"""Tests for sonarr.models.series."""
import json
from datetime import datetime, date, time, timezone

import sonarr.models as models

from . import load_fixture

SERIES = json.loads(load_fixture("series.json"))
SERIESLOOKUP = json.loads(load_fixture("series-lookup.json"))
HISTORY = json.loads(load_fixture("history.json"))
QUEUE = json.loads(load_fixture("queue.json"))
WANTED = json.loads(load_fixture("wanted-missing.json"))
TAG = json.loads(load_fixture("tag.json"))
UTC = timezone.utc


def test_season_statistics() -> None:
    """Test the SeasonStatistics model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 2
    seas0, seas1 = seasons

    stats0 = seas0.statistics
    assert stats0.previousAiring == datetime(2015, 4, 10, 4, 1, tzinfo=UTC)
    assert stats0.episodeFileCount == 13
    assert stats0.episodeCount == 13
    assert stats0.totalEpisodeCount == 13
    assert stats0.sizeOnDisk == 22738179333
    assert stats0.percentOfEpisodes == 100

    stats1 = seas1.statistics
    assert stats1.previousAiring == datetime(2016, 3, 18, 4, 1, tzinfo=UTC)
    assert stats1.episodeFileCount == 13
    assert stats1.episodeCount == 13
    assert stats1.totalEpisodeCount == 13
    assert stats1.sizeOnDisk == 56544094360
    assert stats1.percentOfEpisodes == 100


def test_season() -> None:
    """Test the Season model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 2
    seas0, seas1 = seasons

    assert seas0.seasonNumber == 1
    assert seas0.monitored is False
    # tested in test_season_statistics()
    assert isinstance(seas0.statistics, models.SeasonStatistics)

    assert seas1.seasonNumber == 2
    assert seas1.monitored is False
    # tested in test_season_statistics()
    assert isinstance(seas1.statistics, models.SeasonStatistics)

    # instance returned by /series/lookup
    series = models.Series.from_dict(SERIESLOOKUP[0])
    seasons = series.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 5
    seas0, seas1, seas2, seas3, seas4 = seasons

    assert seas0.seasonNumber == 0
    assert seas0.monitored is False

    assert seas1.seasonNumber == 1
    assert seas1.monitored is False

    assert seas2.seasonNumber == 2
    assert seas2.monitored is False

    assert seas3.seasonNumber == 3
    assert seas3.monitored is False

    assert seas4.seasonNumber == 4
    assert seas4.monitored is False

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(WANTED)
    ep0, ep1 = want.records

    ser0 = ep0.series
    seasons = ser0.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 5
    seas0, seas1, seas2, seas3, seas4 = seasons
    assert seas0.seasonNumber == 4
    assert seas0.monitored is True
    assert seas1.seasonNumber == 3
    assert seas1.monitored is True
    assert seas2.seasonNumber == 2
    assert seas2.monitored is True
    assert seas3.seasonNumber == 1
    assert seas3.monitored is True
    assert seas4.seasonNumber == 0
    assert seas4.monitored is False

    ser1 = ep1.series
    seasons = ser1.seasons
    assert isinstance(seasons, tuple)
    assert len(seasons) == 9
    assert seasons[0].seasonNumber == 0
    assert seasons[0].monitored is False
    assert seasons[1].seasonNumber == 1
    assert seasons[1].monitored is False
    assert seasons[2].seasonNumber == 2
    assert seasons[2].monitored is True
    assert seasons[3].seasonNumber == 3
    assert seasons[3].monitored is False
    assert seasons[4].seasonNumber == 4
    assert seasons[4].monitored is False
    assert seasons[5].seasonNumber == 5
    assert seasons[5].monitored is True
    assert seasons[6].seasonNumber == 6
    assert seasons[6].monitored is True
    assert seasons[7].seasonNumber == 7
    assert seasons[7].monitored is True
    assert seasons[8].seasonNumber == 8
    assert seasons[8].monitored is True

    # instance returned by /queue
    pass  # Identical to 2nd series in /wanted/missing i.e. "Andy Griffith Show"


def test_rating() -> None:
    """Test the Rating model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    ratings = series.ratings
    assert ratings.votes == 461
    assert ratings.value == 8.9

    # instance returned by /series/lookup
    series = models.Series.from_dict(SERIESLOOKUP[0])
    ratings = series.ratings
    assert ratings.votes == 182
    assert ratings.value == 8.6

    # instance returned by /history
    hist = models.History.from_dict(HISTORY)
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ser0 = dl0.series
    rating0 = ser0.ratings
    assert rating0.votes == 51
    assert rating0.value == 8.1

    ser1 = dl1.series
    rating1 = ser1.ratings
    assert rating1.votes == 51
    assert rating1.value == 8.1

    # instance returned by /queue
    item = models.QueueItem.from_dict(QUEUE[0])
    series = item.series
    rating = series.ratings
    assert rating.votes == 547
    assert rating.value == 8.6


def test_alternate_title() -> None:
    """Test the AlternateTitle model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    altTitles = series.alternateTitles
    assert isinstance(altTitles, tuple)
    assert len(altTitles) == 1
    altTitle = altTitles[0]
    assert altTitle.title == "Daredevil"
    assert altTitle.seasonNumber == -1


def test_image() -> None:
    """Test the Image model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    images = series.images
    assert isinstance(images, tuple)
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert img0.url == "/sonarr/MediaCover/7/fanart.jpg?lastWrite=636072351904299472"

    assert img1.coverType == "banner"
    assert img1.url == "/sonarr/MediaCover/7/banner.jpg?lastWrite=636071666185812942"

    assert img2.coverType == "poster"
    assert img2.url == "/sonarr/MediaCover/7/poster.jpg?lastWrite=636071666195067584"

    # instance returned by /series/lookup
    series = models.Series.from_dict(SERIESLOOKUP[0])
    images = series.images
    assert isinstance(images, tuple)
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert img0.url == "http://thetvdb.com/banners/fanart/original/266189-24.jpg"

    assert img1.coverType == "banner"
    assert img1.url == "http://thetvdb.com/banners/graphical/266189-g22.jpg"

    assert img2.coverType == "poster"
    assert img2.url == "http://thetvdb.com/banners/posters/266189-14.jpg"

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(WANTED)
    ep0, ep1 = want.records

    ser0 = ep0.series
    images = ser0.images
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "banner"
    assert img0.url == "http://slurm.trakt.us/images/banners/1387.6.jpg"

    assert img1.coverType == "poster"
    assert img1.url == "http://slurm.trakt.us/images/posters/1387.6-300.jpg"

    assert img2.coverType == "fanart"
    assert img2.url == "http://slurm.trakt.us/images/fanart/1387.6.jpg"

    ser1 = ep1.series
    images = ser1.images
    assert len(images) == 3
    img0, img1, img2 = images

    assert img0.coverType == "fanart"
    assert img0.url == "https://artworks.thetvdb.com/banners/fanart/original/77754-5.jpg"
    assert img1.coverType == "banner"
    assert img1.url == "https://artworks.thetvdb.com/banners/graphical/77754-g.jpg"
    assert img2.coverType == "poster"
    assert img2.url == "https://artworks.thetvdb.com/banners/posters/77754-4.jpg"

    # instance returned by /queue
    pass  # identical to 2nd series from /wanted/missing i.e. "Andy Griffith Show"


def test_tag() -> None:
    """Test the Tag model."""
    # instance returned by /series
    pass  # FIXME - need data

    # instance returned by /tag
    tags = [models.Tag.from_dict(tag) for tag in TAG]
    assert len(tags) == 2
    tag0, tag1 = tags

    assert tag0.label == "amzn"
    assert tag0.id == 1

    assert tag1.label == "netflix"
    assert tag1.id == 2


def test_series() -> None:
    """Test the Series model."""
    # instance returned by /series
    series = models.Series.from_dict(SERIES[0])
    assert series.title == "Marvel's Daredevil"
    assert isinstance(series.alternateTitles, tuple)
    for at in series.alternateTitles:
        assert isinstance(at, models.AlternateTitle)  # tested in test_alternate_title()
    assert series.sortTitle == "marvels daredevil"
    assert series.seasonCount == 2
    assert series.totalEpisodeCount == 26
    assert series.episodeCount == 26
    assert series.episodeFileCount == 26
    assert series.sizeOnDisk == 79282273693
    assert series.status == "continuing"
    assert series.overview == (
        "Matt Murdock was blinded in a tragic accident as a boy, but imbued "
        "with extraordinary senses. Murdock sets up practice in his old "
        "neighborhood of Hell's Kitchen, New York, where he now fights "
        "against injustice as a respected lawyer by day and as the masked "
        "vigilante Daredevil by night."
    )
    assert series.previousAiring == datetime(2016, 3, 18, 4, 1, tzinfo=UTC)
    assert series.network == "Netflix"
    assert series.airTime == time(0, 1)
    assert isinstance(series.images, tuple)
    for at in series.images:
        assert isinstance(at, models.Image)  # tested in test_image()
    assert isinstance(series.seasons, tuple)
    for at in series.seasons:
        assert isinstance(at, models.Season)  # tested in test_season()
    assert series.year == 2015
    assert series.path == "F:\\TV_Shows\\Marvels Daredevil"
    assert series.profileId == 6
    assert series.seasonFolder is True
    assert series.monitored is True
    assert series.useSceneNumbering is False
    assert series.runtime == 55
    assert series.tvdbId == 281662
    assert series.tvRageId == 38796
    assert series.tvMazeId == 1369
    assert series.firstAired == datetime(2015, 4, 10, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-09T09:02:49.4402575Z"
    # Round fractional seconds to microseconds
    assert series.lastInfoSync == datetime(2016, 9, 9, 9, 2, 49, 440258, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "marvelsdaredevil"
    assert series.imdbId == "tt3322312"
    assert series.titleSlug == "marvels-daredevil"
    assert series.certification == "TV-MA"
    assert series.genres == ("Action", "Crime", "Drama")
    assert series.tags == ()
    #  "added": "2015-05-15T00:20:32.7892744Z"
    # Round fractional seconds to microseconds
    assert series.added == datetime(2015, 5, 15, 0, 20, 32, 789274, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 6
    assert series.id == 7

    # instance returned by /series/lookup
    series = models.Series.from_dict(SERIESLOOKUP[0])
    assert series.title == "The Blacklist"
    assert series.sortTitle == "blacklist"
    assert series.seasonCount == 4
    assert series.status == "continuing"
    assert series.overview == (
        '''Raymond "Red" Reddington, one of the FBI's most wanted fugitives, '''
        "surrenders in person at FBI Headquarters in Washington, D.C. He "
        "claims that he and the FBI have the same interests: bringing down "
        "dangerous criminals and terrorists. In the last two decades, he's "
        "made a list of criminals and terrorists that matter the most but the "
        "FBI cannot find because it does not know they exist. Reddington "
        'calls this "The Blacklist".\nReddington will co-operate, but insists '
        "that he will speak only to Elizabeth Keen, a rookie FBI profiler."
    )
    assert series.network == "NBC"
    assert series.airTime == time(21)
    assert isinstance(series.images, tuple)
    for at in series.images:
        assert isinstance(at, models.Image)  # tested in test_image()
    assert series.remotePoster == "http://thetvdb.com/banners/posters/266189-14.jpg"
    assert isinstance(series.seasons, tuple)
    for seas in series.seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert series.year == 2013
    assert series.profileId == 0
    assert series.seasonFolder is False
    assert series.monitored is False
    assert series.useSceneNumbering is False
    assert series.runtime == 45
    assert series.tvdbId == 266189
    assert series.tvRageId == 35048
    assert series.tvMazeId == 69
    assert series.firstAired == datetime(2013, 9, 23, 5, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "theblacklist"
    assert series.imdbId == "tt2741602"
    assert series.titleSlug == "the-blacklist"
    assert series.certification == "TV-14"
    assert series.genres == ("Action", "Crime", "Drama", "Mystery")
    assert series.tags == ()
    assert series.added == datetime(1, 1, 1, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 0

    # instance returned by /wanted/missing
    want = models.WantedMissing.from_dict(WANTED)
    ep0, ep1 = want.records

    ser0 = ep0.series
    assert ser0.tvdbId == 194031
    assert ser0.tvRageId == 24607
    assert ser0.imdbId == "tt1561755"
    assert ser0.title == "Bob's Burgers"
    assert ser0.sortTitle == "bob burgers"
    assert ser0.cleanTitle == "bobsburgers"
    assert ser0.seasonCount == 4
    assert ser0.status == "continuing"
    assert ser0.overview == (
        "Bob's Burgers follows a third-generation restaurateur, Bob, as he "
        "runs Bob's Burgers with the help of his wife and their three kids. "
        "Bob and his quirky family have big ideas about burgers, but fall "
        "short on service and sophistication. Despite the greasy counters, "
        "lousy location and a dearth of customers, Bob and his family are "
        "determined to make Bob's Burgers \"grand re-re-re-opening\" a success."
    )
    assert ser0.airTime == time(17, 30)
    assert ser0.monitored is True
    assert ser0.qualityProfileId == 1
    assert ser0.seasonFolder is True
    assert ser0.lastInfoSync == datetime(2014, 1, 26, 19, 25, 55, 455594, tzinfo=UTC)
    assert ser0.runtime == 30

    images = ser0.images
    assert isinstance(images, tuple)
    for img in images:
        assert isinstance(img, models.Image)  # tested in test_models_image()
    assert ser0.seriesType == "standard"
    assert ser0.network == "FOX"
    assert ser0.useSceneNumbering is False
    assert ser0.titleSlug == "bobs-burgers"
    assert ser0.certification == "TV-14"
    assert ser0.path == "T:\\Bob's Burgers"
    assert ser0.year == 2011
    assert ser0.firstAired == datetime(2011, 1, 10, 1, 30, tzinfo=UTC)
    assert ser0.genres == ("Animation", "Comedy")
    assert ser0.tags == ()
    assert ser0.added == datetime(2011, 1, 26, 19, 25, 55, 455594, tzinfo=UTC)

    #  QualityProfile tested in test_models_quality.test_quality_profile()
    assert isinstance(ser0.qualityProfile, models.QualityProfile)

    seasons = ser0.seasons
    assert isinstance(seasons, tuple)
    for seas in seasons:
        assert isinstance(seas, models.Season)  # tested in test_models_season()
    assert ser0.id == 66

    ser1 = ep1.series
    assert ser1.imdbId == ""
    assert ser1.tvdbId == 77754
    assert ser1.tvRageId == 5574
    assert ser1.tvMazeId == 3853
    assert ser1.title == "The Andy Griffith Show"
    assert ser1.sortTitle == "andy griffith show"
    assert ser1.cleanTitle == "theandygriffithshow"
    assert ser1.seasonCount == 8
    assert ser1.status == "ended"
    assert ser1.overview == (
        "Down-home humor and an endearing cast of characters helped make The "
        "Andy Griffith Show one of the most beloved comedies in the history "
        "of TV. The show centered around widower Andy Taylor, who divided his "
        "time between raising his young son Opie, and his job as sheriff of "
        "the sleepy North Carolina town, Mayberry. Andy and Opie live with "
        "Andy's Aunt Bee, who serves as a surrogate mother to both father and "
        "son. Andy's nervous cousin, Barney Fife, is his deputy sheriff whose "
        "incompetence is tolerated because Mayberry is virtually crime-free."
    )
    assert ser1.airTime == time(21, 30)
    assert ser1.monitored is True
    assert ser1.qualityProfileId == 1
    assert ser1.seasonFolder is True
    assert ser1.lastInfoSync == datetime(2016, 2, 5, 16, 40, 11, 614176, tzinfo=UTC)
    assert ser1.runtime == 25
    images = ser1.images
    assert isinstance(images, tuple)
    for img in images:
        assert isinstance(img, models.Image)  # tested in test_models_image()
    assert ser1.seriesType == "standard"
    assert ser1.network == "CBS"
    assert ser1.useSceneNumbering is False
    assert ser1.titleSlug == "the-andy-griffith-show"
    assert ser1.certification == "TV-G"
    assert ser1.path == "F:\\The Andy Griffith Show"
    assert ser1.year == 1960
    assert ser1.firstAired == datetime(1960, 2, 15, 6, tzinfo=UTC)
    assert ser1.genres == ("Comedy", )
    assert ser1.tags == ()
    assert ser1.added == datetime(2008, 2, 4, 13, 44, 24, 204583, tzinfo=UTC)
    # tested in test_models_quality.test_quality_profile()
    assert isinstance(ser1.qualityProfile, models.QualityProfile)
    seasons = ser1.seasons
    assert isinstance(seasons, tuple)
    for seas in seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert ser1.id == 17

    # Series instance returned by /history
    hist = models.History.from_dict(HISTORY)
    assert len(hist.records) == 2
    dl0, dl1 = hist.records

    ser0 = dl0.series
    assert ser0.title == "Blindspot"
    assert ser0.sortTitle == "blindspot"
    assert ser0.seasonCount == 0
    assert ser0.status == "continuing"
    assert ser0.overview == (
        "A vast international plot explodes when a beautiful Jane Doe is "
        "discovered naked in Times Square, completely covered in "
        "mysterious, intricate tattoos with no memory of who she is or how "
        "she got there. But there's one tattoo that is impossible to miss: "
        "the name of FBI agent Kurt Weller, emblazoned across her back. "
        '"Jane," Agent Weller and the rest of the FBI quickly realize that '
        "each mark on her body is a crime to solve, leading them closer to "
        "the truth about her identity and the mysteries to be revealed."
    )
    assert ser0.network == "NBC"
    assert ser0.airTime == time(20)
    assert ser0.images == ()
    assert ser0.seasons == ()
    assert ser0.year == 2015
    assert ser0.path == "F:\\TV_Shows\\Blindspot"
    assert ser0.profileId == 6
    assert ser0.seasonFolder is True
    assert ser0.monitored is True
    assert ser0.useSceneNumbering is False
    assert ser0.runtime == 45
    assert ser0.tvdbId == 295647
    assert ser0.tvRageId == 0
    assert ser0.tvMazeId == 1855
    assert ser0.firstAired == datetime(2015, 9, 21, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-10T09:03:51.98498Z"
    # 0.98498 seconds == 984980 microseconds
    assert ser0.lastInfoSync == datetime(2016, 9, 10, 9, 3, 51, 984980, tzinfo=UTC)
    assert ser0.seriesType == "standard"
    assert ser0.cleanTitle == "blindspot"
    assert ser0.imdbId == "tt4474344"
    assert ser0.titleSlug == "blindspot"
    assert ser0.certification == "TV-14"
    assert ser0.genres == ()
    assert ser0.tags == (2, )
    # "added": "2015-08-13T01:36:54.4303036Z"
    # Round to milliseconds
    assert ser0.added == datetime(2015, 8, 13, 1, 36, 54, 430304, tzinfo=UTC)
    assert isinstance(ser0.ratings, models.Rating)  # tested in test_rating()
    assert ser0.qualityProfileId == 6
    assert ser0.id == 60

    ser1 = dl1.series
    assert ser1.title == "Blindspot"
    assert ser1.sortTitle == "blindspot"
    assert ser1.seasonCount == 0
    assert ser1.status == "continuing"
    assert ser1.overview == (
        "A vast international plot explodes when a beautiful Jane Doe is "
        "discovered naked in Times Square, completely covered in mysterious, "
        "intricate tattoos with no memory of who she is or how she got there. "
        "But there's one tattoo that is impossible to miss: the name of FBI "
        'agent Kurt Weller, emblazoned across her back. "Jane," Agent Weller '
        "and the rest of the FBI quickly realize that each mark on her body "
        "is a crime to solve, leading them closer to the truth about her "
        "identity and the mysteries to be revealed."
    )
    assert ser1.network == "NBC"
    assert ser1.airTime == time(20)
    assert ser1.images == ()
    assert ser1.seasons == ()
    assert ser1.year == 2015
    assert ser1.path == "F:\\TV_Shows\\Blindspot"
    assert ser1.profileId == 6
    assert ser1.seasonFolder is True
    assert ser1.monitored is True
    assert ser1.useSceneNumbering is False
    assert ser1.runtime == 45
    assert ser1.tvdbId == 295647
    assert ser1.tvRageId == 0
    assert ser1.tvMazeId == 1855
    assert ser1.firstAired == datetime(2015, 9, 21, 4, tzinfo=UTC)
    # "lastInfoSync": "2016-09-10T09:03:51.98498Z"
    # 0.98498 seconds == 984980 microseconds
    assert ser1.lastInfoSync == datetime(2016, 9, 10, 9, 3, 51, 984980, tzinfo=UTC)
    assert ser1.seriesType == "standard"
    assert ser1.cleanTitle == "blindspot"
    assert ser1.imdbId == "tt4474344"
    assert ser1.titleSlug == "blindspot"
    assert ser1.certification == "TV-14"
    assert ser1.genres == ()
    assert ser1.tags == (2, )
    # "added": "2015-08-13T01:36:54.4303036Z"
    # Round to microseconds
    assert ser1.added == datetime(2015, 8, 13, 1, 36, 54, 430304, tzinfo=UTC)
    assert isinstance(ser1.ratings, models.Rating)  # tested in test_rating()
    assert ser1.qualityProfileId == 6
    assert ser1.id == 60

    # Series instance returned by /parse
    pass  # FIXME - need data

    # Series instance returned by /queue
    item = models.QueueItem.from_dict(QUEUE[0])
    series = item.series

    assert series.title == "The Andy Griffith Show"
    assert series.sortTitle == "andy griffith show"
    assert series.seasonCount == 8
    assert series.status == "ended"
    assert series.overview == (
        "Down-home humor and an endearing cast of characters helped make The "
        "Andy Griffith Show one of the most beloved comedies in the history "
        "of TV. The show centered around widower Andy Taylor, who divided his "
        "time between raising his young son Opie, and his job as sheriff of "
        "the sleepy North Carolina town, Mayberry. Andy and Opie live with "
        "Andy's Aunt Bee, who serves as a surrogate mother to both father and "
        "son. Andy's nervous cousin, Barney Fife, is his deputy sheriff whose "
        "incompetence is tolerated because Mayberry is virtually crime-free."
    )
    assert series.network == "CBS"
    assert series.airTime == time(21, 30)
    assert isinstance(series.images, tuple)
    for img in series.images:
        assert isinstance(img, models.Image)  # tested in test_image()
    assert isinstance(series.seasons, tuple)
    for seas in series.seasons:
        assert isinstance(seas, models.Season)  # tested in test_season()
    assert series.year == 1960
    assert series.path == "F:\\The Andy Griffith Show"
    assert series.profileId == 5
    assert series.seasonFolder is True
    assert series.monitored is True
    assert series.useSceneNumbering is False
    assert series.runtime == 25
    assert series.tvdbId == 77754
    assert series.tvRageId == 5574
    assert series.tvMazeId == 3853
    assert series.firstAired == datetime(1960, 2, 15, 6, tzinfo=UTC)
    assert series.lastInfoSync == datetime(2016, 2, 5, 16, 40, 11, 614176, tzinfo=UTC)
    assert series.seriesType == "standard"
    assert series.cleanTitle == "theandygriffithshow"
    assert series.imdbId == ""
    assert series.titleSlug == "the-andy-griffith-show"
    assert series.certification == "TV-G"
    assert series.genres == ("Comedy", )
    assert series.tags == ()
    assert series.added == datetime(2008, 2, 4, 13, 44, 24, 204583, tzinfo=UTC)
    assert isinstance(series.ratings, models.Rating)  # tested in test_rating()
    assert series.qualityProfileId == 5
    assert series.id == 17
