"""Tests for Sonarr."""
from typing import List

import pytest
from aiohttp import ClientSession

from sonarr import Sonarr
from sonarr.models import Episode, QueueItem, SeriesItem, Series, Season, WantedResults
from tests import load_fixture

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8989

MATCH_HOST = f"{HOST}:{PORT}"


@pytest.mark.asyncio
async def test_calendar(aresponses):
    """Test calendar method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/v3/calendar?start=2014-01-26&end=2014-01-27",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("sonarr/calendar.json"),
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.calendar("2014-01-26", "2014-01-27")

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], Episode)


@pytest.mark.asyncio
async def test_queue(aresponses):
    """Test queue method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/v3/queue",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("sonarr/queue.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.queue()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], QueueItem)
        assert response[0].episode
        assert isinstance(response[0].episode, Episode)


@pytest.mark.asyncio
async def test_series(aresponses):
    """Test series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/v3/series",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("sonarr/series.json"),
        ),
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.series()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], SeriesItem)
        assert response[0].series
        assert isinstance(response[0].series, Series)

        assert response[0].seasons
        assert isinstance(response[0].seasons, List)

        assert response[0].seasons[0]
        assert isinstance(response[0].seasons[0], Season)


@pytest.mark.asyncio
async def test_wanted(aresponses):
    """Test queue method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/v3/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDir=desc",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("sonarr/wanted-missing.json"),
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Sonarr(HOST, API_KEY, session=session)
        response = await client.wanted()

        assert response
        assert isinstance(response, WantedResults)

        assert response.page == 1
        assert response.per_page == 10
        assert response.total == 2
        assert response.sort_key == "airDateUtc"
        assert response.sort_dir == "descending"

        assert response.episodes
        assert isinstance(response.episodes, List)
        assert len(response.episodes) == 2

        assert response.episodes[0]
        assert isinstance(response.episodes[0], Episode)
