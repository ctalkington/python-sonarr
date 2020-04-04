"""Tests for Sonarr."""
from typing import List

import pytest
from aiohttp import ClientSession
from sonarr import Sonarr
from sonarr.models import Application, Info

from . import load_fixture

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8989

MATCH_HOST = f"{HOST}:{PORT}"


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
        assert isinstance(client.app, Application)


@pytest.mark.asyncio
async def test_update(aresponses):
    """Test update is handled correctly."""
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
        response = await client.update()

        assert response
        assert isinstance(response.info, Info)
        assert isinstance(response.disks, List)

        response = await client.update()

        assert response
        assert isinstance(response.info, Info)
        assert isinstance(response.disks, List)
