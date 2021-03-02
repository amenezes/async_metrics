from async_metrics import logger

try:
    from async_metrics.ext import aiohttp
except ImportError:
    logger.error("AIOHTTP dependency not found!")

from async_metrics.ext.flask import flask

__all__ = ["aiohttp", "flask"]
