try:
    from async_metrics.ext.flask.flask import setup_async_metrics
except ImportError as err:
    flask = None
