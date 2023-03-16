import pytest
from aiohttp import web

from async_metrics.ext.aiohttp import setup_async_metrics


@pytest.fixture
async def aiohttp_app():
    app = web.Application()
    setup_async_metrics(app)
    return app


@pytest.mark.parametrize(
    "uri,status_code,mimetype",
    [
        ("/async_metrics/dashboard", 200, "text/html"),
        ("/async_metrics/all", 200, "application/json"),
        ("/async_metrics/asyncio", 200, "application/json"),
        ("/async_metrics/system", 200, "application/json"),
        ("/async_metrics/system/dependencies", 200, "application/json"),
        ("/async_metrics/system/python", 200, "application/json"),
        ("/async_metrics/system/process", 200, "application/json"),
        ("/async_metrics/system/partitions", 200, "application/json"),
        ("/async_metrics/routes", 200, "application/json"),
        ("/async_metrics/about", 200, "application/json"),
    ],
)
async def test_aiohttp_integration(
    aiohttp_client, aiohttp_app, uri, status_code, mimetype
):
    client = await aiohttp_client(aiohttp_app)
    resp = await client.get(uri)
    assert resp.status == status_code
    assert resp.content_type == mimetype


@pytest.mark.parametrize(
    "uri,status_code,mimetype",
    [
        ("/custom/dashboard", 200, "text/html"),
        ("/custom/all", 200, "application/json"),
        ("/custom/asyncio", 200, "application/json"),
        ("/custom/system", 200, "application/json"),
        ("/custom/system/dependencies", 200, "application/json"),
        ("/custom/system/python", 200, "application/json"),
        ("/custom/system/process", 200, "application/json"),
        ("/custom/system/partitions", 200, "application/json"),
        ("/custom/routes", 200, "application/json"),
        ("/custom/about", 200, "application/json"),
    ],
)
async def test_aiohttp_with_custom_name(aiohttp_client, uri, status_code, mimetype):
    app = web.Application()
    setup_async_metrics(app, "custom")
    client = await aiohttp_client(app)
    resp = await client.get(uri)
    assert resp.status == status_code
    assert resp.content_type == mimetype
