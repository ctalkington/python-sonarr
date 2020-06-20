"""Tests for Sonarr."""
from typing import List

import pytest
import sonarr.models as models
from aiohttp import ClientSession
from sonarr import Sonarr

from . import load_fixture

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8989

MATCH_HOST = f"{HOST}:{PORT}"


@pytest.mark.asyncio
async def test_loop():
    """Test loop usage is handled correctly."""
    async with Sonarr(HOST, API_KEY) as sonarr:
        assert isinstance(sonarr, Sonarr)


@pytest.mark.asyncio
async def test_app(aresponses):
    """Test app property is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("system-status.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("diskspace.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        await client.update()

        assert client.app
        assert isinstance(client.app, models.Application)


@pytest.mark.asyncio
async def test_calendar(aresponses):
    """Test calendar method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/calendar?start=2014-01-26&end=2014-01-27",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("calendar.json"),
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.calendar("2014-01-26", "2014-01-27")

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], models.Episode)


@pytest.mark.asyncio
async def test_commands(aresponses):
    """Test commands method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("command.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.commands()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], models.CommandItem)


@pytest.mark.asyncio
async def test_command_status(aresponses):
    """Test command_status method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/command/368630",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("command-id.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.command_status(368630)

        assert response
        assert isinstance(response, models.CommandItem)


@pytest.mark.asyncio
async def test_queue(aresponses):
    """Test queue method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/queue",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("queue.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.queue()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], models.QueueItem)
        assert response[0].episode
        assert isinstance(response[0].episode, models.Episode)


@pytest.mark.asyncio
async def test_series(aresponses):
    """Test series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/series",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("series.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.series()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], models.SeriesItem)
        assert response[0].series
        assert isinstance(response[0].series, models.Series)

        assert response[0].seasons
        assert isinstance(response[0].seasons, List)

        assert response[0].seasons[0]
        assert isinstance(response[0].seasons[0], models.Season)


@pytest.mark.asyncio
async def test_update(aresponses):
    """Test update method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("system-status.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("diskspace.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("diskspace.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.update()

        assert response
        assert isinstance(response.info, models.Info)
        assert isinstance(response.disks, List)

        response = await client.update()

        assert response
        assert isinstance(response.info, models.Info)
        assert isinstance(response.disks, List)


@pytest.mark.asyncio
async def test_wanted(aresponses):
    """Test queue method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDir=desc",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("wanted-missing.json"),
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.wanted()

        assert response
        assert isinstance(response, models.WantedResults)

        assert response.page == 1
        assert response.per_page == 10
        assert response.total == 2
        assert response.sort_key == "airDateUtc"
        assert response.sort_dir == "descending"

        assert response.episodes
        assert isinstance(response.episodes, List)
        assert len(response.episodes) == 2

        assert response.episodes[0]
        assert isinstance(response.episodes[0], models.Episode)
