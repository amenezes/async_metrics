import logging

from flask import Flask

from async_metrics.ext.flask import setup_async_metrics


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
setup_async_metrics(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'
