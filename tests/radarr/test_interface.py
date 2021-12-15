"""Tests for Sonarr."""
from typing import List

import pytest

from aiohttp import ClientSession

from radarr import Radarr
from radarr.models import Movie, QueueItem, MovieFile
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
        "/api/calendar?start=2014-01-26&end=2014-01-27",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("radarr/calendar.json"),
        ),
        match_querystring=True,
    )

    async with ClientSession() as session:
        client = Radarr(HOST, API_KEY, session=session)
        response = await client.calendar("2014-01-26", "2014-01-27")

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], Movie)


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
            text=load_fixture("radarr/queue.json"),
        ),
    )

    async with ClientSession() as session:
        client = Radarr(HOST, API_KEY, session=session)
        response = await client.queue()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], QueueItem)
        assert response[0].episode
        assert isinstance(response[0].episode, Movie)


@pytest.mark.asyncio
async def test_movie(aresponses):
    """Test series method is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/movie",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("radarr/movie.json"),
        ),
    )

    async with ClientSession() as session:
        client = Radarr(HOST, API_KEY, session=session)
        response = await client.series()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], MovieFile)
        assert response[0].series
        assert isinstance(response[0].series, Movie)
