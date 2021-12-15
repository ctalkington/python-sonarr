"""Tests for Sonarr."""
from typing import List

import pytest

from aiohttp import ClientSession

from arr import Client
from arr.models import Application, CommandItem, QueueItem, Info, WantedResults

from tests import load_fixture

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8080

MATCH_HOST = f"{HOST}:{PORT}"


@pytest.mark.asyncio
async def test_loop():
    """Test loop usage is handled correctly."""
    async with Client(HOST, API_KEY) as client:
        assert isinstance(client, Client)


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
            text=load_fixture("arr/system-status.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("arr/diskspace.json"),
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        await client.update()

        assert client.app
        assert isinstance(client.app, Application)


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
            text=load_fixture("arr/command.json"),
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client.commands()

        assert response
        assert isinstance(response, List)

        assert response[0]
        assert isinstance(response[0], CommandItem)


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
            text=load_fixture("arr/command-id.json"),
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client.command_status(368630)

        assert response
        assert isinstance(response, CommandItem)


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
            text=load_fixture("arr/system-status.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("arr/diskspace.json"),
        ),
    )

    aresponses.add(
        MATCH_HOST,
        "/api/diskspace",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("arr/diskspace.json"),
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client.update()

        assert response
        assert isinstance(response.info, Info)
        assert isinstance(response.disks, List)

        response = await client.update()

        assert response
        assert isinstance(response.info, Info)
        assert isinstance(response.disks, List)
