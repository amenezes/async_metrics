from aiohttp.web import HTTPForbidden, middleware

from async_metrics.ext.utils import Forbidden, private_ip_validator


@middleware
async def restrict_access(request, handler):
    try:
        private_ip_validator(request.remote)
    except Forbidden:
        raise HTTPForbidden
    resp = await handler(request)
    return resp
