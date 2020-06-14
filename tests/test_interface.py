"""Tests for Sonarr."""
from datetime import datetime, date, timezone

import pytest
import sonarr.models as models
#  from aiohttp import ClientSession
from aiohttp import ClientSession
from sonarr import Sonarr

from . import load_fixture

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8989
MATCH_HOST = f"{HOST}:{PORT}"

UTC = timezone.utc

CALENDAR = load_fixture("calendar.json")
COMMAND = load_fixture("command.json")
COMMANDID = load_fixture("command-id.json")
DISKSPACE = load_fixture("diskspace.json")
EPISODE = load_fixture("episode.json")
EPISODEID = load_fixture("episode-id.json")
EPISODEFILE = load_fixture("episodefile.json")
EPISODEFILEID = load_fixture("episodefile-id.json")
HISTORY = load_fixture("history.json")
PARSE = load_fixture("parse.json")
PROFILE = load_fixture("profile.json")
QUEUE = load_fixture("queue.json")
RELEASE = load_fixture("release.json")
ROOTFOLDER = load_fixture("rootfolder.json")
SERIES = load_fixture("series.json")
SERIESID = load_fixture("series-id.json")
SERIESPOST = load_fixture("series-post.json")
SERIESLOOKUP = load_fixture("series-lookup.json")
SYSTEMSTATUS = load_fixture("system-status.json")
SYSTEMBACKUP = load_fixture("system-backup.json")
TAG = load_fixture("tag.json")
TAGID = load_fixture("tag-id.json")
WANTEDMISSING = load_fixture("wanted-missing.json")


@pytest.mark.asyncio
async def test_get_calendar(aresponses):
    """Test get_calendar method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/calendar?start=2014-01-26&end=2014-01-27",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=CALENDAR,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_calendar(date(2014, 1, 26), date(2014, 1, 27))

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.Episode)


@pytest.mark.asyncio
async def test_get_all_commands(aresponses):
    """Test get_all_commands method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMAND,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_all_commands()

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.CommandStatus)


@pytest.mark.asyncio
async def test_get_command(aresponses):
    """Test get_command method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command/368630",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_command(368630)

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_refresh_all_series(aresponses):
    """Test refresh_all_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.refresh_all_series()

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_refresh_series(aresponses):
    """Test refresh_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.refresh_series(1)

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_rescan_all_series(aresponses):
    """Test rescan_all_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.rescan_all_series()

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_rescan_series(aresponses):
    """Test rescan_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.rescan_series(1)

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_search_episodes(aresponses):
    """Test search_episodes method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.search_episodes([1, 2, 3])

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_search_season(aresponses):
    """Test search_season method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.search_season(seriesId=1, seasonNumber=2)

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_search_series(aresponses):
    """Test foo method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.search_series(1)

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_sync_rss(aresponses):
    """Test sync_rss method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.sync_rss()

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_rename_files(aresponses):
    """Test rename_files method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.rename_files([123, 345, 567])

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_rename_series(aresponses):
    """Test rename_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.rename_series([123, 345, 567])

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_backup(aresponses):
    """Test backup method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.backup()

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_search_missing_episodes(aresponses):
    """Test search_missing_episodes method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=COMMANDID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.search_missing_episodes()

        assert response
        assert isinstance(response, models.CommandStatus)


@pytest.mark.asyncio
async def test_get_diskspace(aresponses):
    """Test get_diskspace method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=DISKSPACE,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_diskspace()

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.DiskSpace)


@pytest.mark.asyncio
async def test_get_episodes(aresponses):
    """Test get_episodes method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episode?seriesId=1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODE,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_episodes(seriesId=1)

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.Episode)


@pytest.mark.asyncio
async def test_get_episode(aresponses):
    """Test get_episode method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episode/1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODEID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_episode(1)

        assert response
        assert isinstance(response, models.Episode)


@pytest.mark.asyncio
async def test_update_episode(aresponses):
    """Test update_episode method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episode",
        "PUT",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODEID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)

        episode = models.Episode(
            seriesId=1,
            episodeFileId=0,
            seasonNumber=1,
            episodeNumber=1,
            title="Mole Hunt",
            airDate=date(2009, 9, 17),
            airDateUtc=datetime(2009, 9, 18, 2, tzinfo=UTC),
            overview=(
                "Archer is in trouble with his Mother and the Comptroller because his "
                "expense account is way out of proportion to his actual expenses. So "
                "he creates the idea that a Mole has breached ISIS and he needs to get"
                " into the mainframe to hunt him down (so he can cover his tracks!). "
                "All this leads to a surprising ending."
            ),
            hasFile=False,
            monitored=True,
            sceneEpisodeNumber=0,
            sceneSeasonNumber=0,
            tvDbEpisodeId=0,
            absoluteEpisodeNumber=1,
            id=1,
        )
        response = await client.update_episode(episode)

        assert response
        assert isinstance(response, models.Episode)


@pytest.mark.asyncio
async def test_get_episode_files(aresponses):
    """Test get_episode_files method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episodefile?seriesId=1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODEFILE,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_episode_files(seriesId=1)

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.EpisodeFile)


@pytest.mark.asyncio
async def test_get_episode_file(aresponses):
    """Test get_episode_file method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episodefile/1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODEFILEID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_episode_file(1)

        assert response
        assert isinstance(response, models.EpisodeFile)


@pytest.mark.asyncio
async def test_delete_episode_file(aresponses):
    """Test delete_episode_file method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episodefile/1",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="{}",
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.delete_episode_file(1)
        assert response is True


@pytest.mark.asyncio
async def test_update_episode_file(aresponses):
    """Test update_episode_file method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/episodefile/1",
        "PUT",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=EPISODEFILEID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        quality = models.QualityRevision(
            quality=models.Quality(id=8),
            revision=models.Revision(version=1, real=0)
        )
        response = await client.update_episode_file(1, quality)
        assert isinstance(response, models.EpisodeFile)


@pytest.mark.asyncio
async def test_get_history(aresponses):
    """Test get_history method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/history?sortKey=date&page=1&pageSize=10&sortDir=desc",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=HISTORY,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_history(sortDir=models.SortDirection.DESCENDING)

        assert response
        assert isinstance(response, models.History)

        assert response.page == 1
        assert response.pageSize == 10
        assert response.totalRecords == 8094
        assert response.sortKey is models.SortKey.DATE
        assert response.sortDirection is models.SortDirection.DESCENDING

        assert response.records
        assert isinstance(response.records, tuple)
        assert len(response.records) == 2

        for record in response.records:
            assert isinstance(record, models.Download)


@pytest.mark.asyncio
async def test_get_wanted_missing(aresponses):
    """Test get_wanted_missing method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDir=desc",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=WANTEDMISSING,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_wanted_missing()

        assert response
        assert isinstance(response, models.WantedMissing)

        assert response.page == 1
        assert response.pageSize == 10
        assert response.totalRecords == 2
        assert response.sortKey is models.SortKey.AIRDATE
        assert response.sortDirection is models.SortDirection.DESCENDING

        assert response.records
        assert isinstance(response.records, tuple)
        assert len(response.records) == 2

        for record in response.records:
            assert isinstance(record, models.Episode)


@pytest.mark.asyncio
async def test_get_queue(aresponses):
    """Test get_queue method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/queue",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=QUEUE,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_queue()

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.QueueItem)
        assert response[0].episode
        assert isinstance(response[0].episode, models.Episode)


@pytest.mark.asyncio
async def test_delete_queue_item(aresponses):
    """Test delete_queue_item method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/queue",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="{}",
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.delete_queue_item(1)
        assert response is True


@pytest.mark.asyncio
async def test_parse_title(aresponses):
    """Test parse_title method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/parse?title=Series.Title.S01E01.720p.HDTV-Sonarr",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=PARSE,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.parse_title("Series.Title.S01E01.720p.HDTV-Sonarr")

        assert response
        assert isinstance(response, models.ParseResult)


@pytest.mark.asyncio
async def test_parse_path(aresponses):
    """Test parse_path method is handled correctly."""
    pass  # FIXME - need data


@pytest.mark.asyncio
async def test_get_profiles(aresponses):
    """Test get_profiles method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/profile",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=PROFILE,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_profiles()

        assert response
        assert isinstance(response, tuple)

        for profile in response:
            assert isinstance(profile, models.QualityAllowedProfile)


@pytest.mark.asyncio
async def test_get_release(aresponses):
    """Test get_release method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/release?episodeId=1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=RELEASE,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_release(episodeId=1)

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.Release)


@pytest.mark.asyncio
async def test_add_release(aresponses):
    """Test add_release method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/release",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=RELEASE,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.add_release(guid="a5a4a6a7-f7c9-4ff0-b3c4-b8dea9ed965b", indexerId=5)

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.Release)


@pytest.mark.asyncio
async def test_push_release(aresponses):
    """Test push_release method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/release/push",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=RELEASE,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.push_release(
            title="The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV",
            downloadUrl="http://www.newshost.co.za/nzb/5a6/The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV.nzb",
            protocol=models.Protocol.USENET,
            publishDate=datetime(2014, 2, 10, tzinfo=UTC)
        )

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.Release)


@pytest.mark.asyncio
async def test_get_rootfolders(aresponses):
    """Test get_rootfolders method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/rootfolder",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=ROOTFOLDER,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_rootfolders()

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.RootFolder)


@pytest.mark.asyncio
async def test_get_all_series(aresponses):
    """Test get_all_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SERIES,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_all_series()

        assert response
        assert isinstance(response, tuple)

        assert response[0]
        assert isinstance(response[0], models.Series)

        assert response[0].seasons
        assert isinstance(response[0].seasons, tuple)

        assert response[0].seasons[0]
        assert isinstance(response[0].seasons[0], models.Season)


@pytest.mark.asyncio
async def test_get_series(aresponses):
    """Test get_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series/3",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SERIESID,
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_series(3)

        assert response
        assert isinstance(response, models.Series)


@pytest.mark.asyncio
async def test_add_series(aresponses):
    """Test add_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SERIESPOST,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.add_series(
            tvdbId=110381,
            title="Archer (2009)",
            profileId=1,
            titleSlug="archer-2009",
            seasons=(
                models.Season(seasonNumber=5, monitored=True),
                models.Season(seasonNumber=4, monitored=True),
                models.Season(seasonNumber=3, monitored=True),
                models.Season(seasonNumber=2, monitored=True),
                models.Season(seasonNumber=1, monitored=True),
                models.Season(seasonNumber=0, monitored=False),
            ),
            path="T:\\Archer (2009)",
        )

        assert response
        assert isinstance(response, models.Series)


@pytest.mark.asyncio
async def test_update_series(aresponses):
    """Test update_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series",
        "PUT",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SERIESPOST,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)

        series = models.Series(
            tvdbId=110381,
            title="Archer (2009)",
            cleanTitle="archer2009",
            monitored=True,
            seasonFolder=True,
            titleSlug="archer-2009",
            profileId=1,
            seasons=(
                models.Season(seasonNumber=5, monitored=True),
                models.Season(seasonNumber=4, monitored=True),
                models.Season(seasonNumber=3, monitored=True),
                models.Season(seasonNumber=2, monitored=True),
                models.Season(seasonNumber=1, monitored=True),
                models.Season(seasonNumber=0, monitored=False),
            ),
            path="T:\\Archer (2009)",
        )

        response = await client.update_series(series)

        assert response
        assert isinstance(response, models.Series)


@pytest.mark.asyncio
async def test_delete_series(aresponses):
    """Test delete_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series/1",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="{}",
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.delete_series(1)

        assert response is True


@pytest.mark.asyncio
async def test_lookup_series(aresponses):
    """Test lookup_series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series/lookup?term=The%20Blacklist",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SERIESLOOKUP,
        ),
        match_querystring=True,
    )

    async def on_request_start(session, trace_config_ctx, params):
        raise ValueError(params.url, dir(params.url), params.url.query_string)

    async def on_request_end(session, trace_config_ctx, params):
        raise ValueError(params.url, dir(params.url), params.url.query_string)

    #  trace_config = TraceConfig()
    #  trace_config.on_request_start.append(on_request_start)
    #  trace_config.on_request_end.append(on_request_end)

    #  async with ClientSession(trace_configs=[trace_config]) as session:
    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.lookup_series("The Blacklist")

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.Series)


@pytest.mark.asyncio
async def test_get_system_status(aresponses):
    """Test get_system_status method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SYSTEMSTATUS,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_system_status()

        assert response
        assert isinstance(response, models.SystemStatus)


@pytest.mark.asyncio
async def test_get_system_backups(aresponses):
    """Test get_system_backups method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/backup",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=SYSTEMBACKUP,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_system_backups()

        assert response
        assert isinstance(response, tuple)
        assert isinstance(response[0], models.SystemBackup)


@pytest.mark.asyncio
async def test_get_tags(aresponses):
    """Test get_tags method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/tag",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=TAG,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_tags()

        assert response
        assert isinstance(response, tuple)
        for instance in response:
            assert isinstance(instance, models.Tag)


@pytest.mark.asyncio
async def test_get_tag(aresponses):
    """Test get_tag method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/tag/1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=TAGID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.get_tag(1)

        assert response
        assert isinstance(response, models.Tag)


@pytest.mark.asyncio
async def test_add_tag(aresponses):
    """Test add_tag method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/tag",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=TAGID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.add_tag("amzn")

        assert response
        assert isinstance(response, models.Tag)


@pytest.mark.asyncio
async def test_update_tag(aresponses):
    """Test update_tag method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/tag",
        "PUT",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=TAGID,
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.update_tag(1, "amzn")

        assert response
        assert isinstance(response, models.Tag)


@pytest.mark.asyncio
async def test_delete_tag(aresponses):
    """Test delete_tag method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/tag/1",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="{}",
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.delete_tag(1)

        assert response is True
