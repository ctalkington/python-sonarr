"""Tests for Sonarr."""
import asyncio

import pytest
from aiohttp import ClientSession
from sonarr import Client
from sonarr.exceptions import (
    SonarrAccessRestricted,
    SonarrConnectionError,
    SonarrError,
    SonarrResourceNotFound,
)

API_KEY = "MOCK_API_KEY"
HOST = "192.168.1.89"
PORT = 8989

MATCH_HOST = f"{HOST}:{PORT}"
NON_STANDARD_PORT = 3333


@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "OK"}',
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client._request("system/status")
        assert response["status"] == "OK"


@pytest.mark.asyncio
async def test_text_request(aresponses):
    """Test non JSON response is handled correctly."""
    aresponses.add(
        MATCH_HOST, "/api/text", "GET", aresponses.Response(status=200, text="OK"),
    )
    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client._request("text")
        assert response == "OK"


@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test JSON response is handled correctly with internal session."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "OK"}',
        ),
    )

    async with Client(HOST, API_KEY) as client:
        response = await client._request("system/status")
        assert response["status"] == "OK"


@pytest.mark.asyncio
async def test_post_request(aresponses):
    """Test POST requests are handled correctly."""
    aresponses.add(
        MATCH_HOST, "/api/post", "POST", aresponses.Response(status=200, text="OK")
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        response = await client._request("post", method="POST")
        assert response == "OK"


@pytest.mark.asyncio
async def test_request_port(aresponses):
    """Test the handling of non-standard API port."""
    aresponses.add(
        f"{HOST}:{NON_STANDARD_PORT}",
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "OK"}',
        ),
    )

    async with ClientSession() as session:
        client = Client(
            host=HOST, api_key=API_KEY, port=NON_STANDARD_PORT, session=session
        )
        response = await client._request("system/status")
        assert response["status"] == "OK"


@pytest.mark.asyncio
async def test_request_base_path(aresponses):
    """Test API running on different base path."""
    aresponses.add(
        MATCH_HOST,
        "/api/v3/system/status",
        "GET",
        aresponses.Response(text="GOTCHA!", status=200),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, base_path="/api/v3", session=session)
        response = await client._request("system/status")
        assert response == "GOTCHA!"


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from the API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Timeout!")

    aresponses.add(MATCH_HOST, "/api/system/status", "GET", response_handler)

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session, request_timeout=1)
        with pytest.raises(SonarrConnectionError):
            assert await client._request("system/status")


@pytest.mark.asyncio
async def test_client_error():
    """Test HTTP client error."""
    async with ClientSession() as session:
        client = Client("#", API_KEY, session=session)
        with pytest.raises(SonarrConnectionError):
            assert await client._request("system/status")


@pytest.mark.asyncio
async def test_http_error403(aresponses):
    """Test HTTP 403 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(text="Forbidden", status=403),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        with pytest.raises(SonarrAccessRestricted):
            assert await client._request("system/status")


@pytest.mark.asyncio
async def test_http_error404(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(text="Not Found!", status=404),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        with pytest.raises(SonarrResourceNotFound):
            assert await client._request("system/status")


@pytest.mark.asyncio
async def test_http_error500(aresponses):
    """Test HTTP 500 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(text="Internal Server Error", status=500),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        with pytest.raises(SonarrError):
            assert await client._request("system/status")


@pytest.mark.asyncio
async def test_http_error500_json(aresponses):
    """Test HTTP 500 json response handling."""
    aresponses.add(
        MATCH_HOST,
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=500,
            headers={"Content-Type": "application/json"},
            body='{"status": "NOK"}',
        ),
    )

    async with ClientSession() as session:
        client = Client(HOST, API_KEY, session=session)
        with pytest.raises(SonarrError):
            response = await client._request("system/status")
            assert response
            assert response["status"] == "NOK"
