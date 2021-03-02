from async_metrics import logger

try:
    from async_metrics.ext.flask.flask import setup_async_metrics
except ImportError as err:
    logger.error("Flask dependency not found!")
    flask = None
