import logging

from aiohttp import web

from async_metrics.ext.aiohttp import setup_async_metrics


logging.basicConfig(level=logging.INFO)

async def hello(request):
    return web.Response(body='main app')


app = web.Application()
app.add_routes([web.get('/', hello)])
setup_async_metrics(app)
web.run_app(app)
