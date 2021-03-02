import os

from flask import Blueprint, jsonify, make_response, render_template, request

import async_metrics


def setup_async_metrics(app, name: str = "async_metrics"):
    async_metrics = Blueprint(
        "async_metrics",
        "async_metrics",
        name,
        template_folder=os.path.join(os.getcwd(), "async_metrics/ext/flask/templates"),
    )
    configure_routes(async_metrics, name)
    app.register_blueprint(async_metrics)


def configure_routes(bp, name):
    @bp.route(f"/{name}/summary", methods=["GET", "HEAD"])
    def summary():
        return render_template(
            "summary.html",
            version=async_metrics.__version__,
            url=f"{request.scheme}://{request.host}/async_metrics/routes",
        )

    @bp.route(f"/{name}/all", methods=["GET", "HEAD"])
    def all():
        return jsonify(
            {
                "system": async_metrics.sys.all(),
            }
        )

    @bp.route(f"/{name}/system", methods=["GET", "HEAD"])
    def system():
        return jsonify({"system": async_metrics.sys.all()})

    @bp.route(f"/{name}/system/dependencies", methods=["GET", "HEAD"])
    def dependencies():
        return jsonify(async_metrics.sys.packages())

    @bp.route(f"/{name}/system/python", methods=["GET", "HEAD"])
    def python():
        return jsonify(async_metrics.sys.python())

    @bp.route(f"/{name}/system/partitions", methods=["GET", "HEAD"])
    def partitions():
        return jsonify(async_metrics.sys.partitions())

    @bp.route(f"/{name}/system/process", methods=["GET", "HEAD"])
    def process():
        return jsonify(async_metrics.sys.process())

    @bp.route(f"/{name}/about", methods=["GET", "HEAD"])
    def about():
        return jsonify(
            {
                "async_metrics_version": async_metrics.__version__,
                "project_url": "https://github.com/amenezes/async_metrics",
                "issues": "https://github.com/amenezes/async_metrics/issues",
            }
        )

    @bp.route(f"/{name}/routes", methods=["GET", "HEAD"])
    def routes():
        routes = [
            {
                "name": "async_metrics_summary",
                "method": "HEAD",
                "path": "/async_metrics",
                "description": "Show async_metrics available.",
            },
            {
                "name": "async_metrics_summary",
                "method": "GET",
                "path": "/async_metrics",
                "description": "Show async_metrics available.",
            },
            {
                "name": "async_metrics_summary",
                "method": "HEAD",
                "path": "/async_metrics/all",
                "description": "Show information about system environment.",
            },
            {
                "name": "async_metrics_summary",
                "method": "GET",
                "path": "/async_metrics/all",
                "description": "Show information about system environment.",
            },
            {
                "name": "async_metrics_system",
                "method": "HEAD",
                "path": "/async_metrics/system",
                "description": "Show information about system environment.",
            },
            {
                "name": "async_metrics_system",
                "method": "GET",
                "path": "/async_metrics/system",
                "description": "Show information about system environment.",
            },
            {
                "name": "async_metrics_dependencies",
                "method": "HEAD",
                "path": "/async_metrics/system/dependencies",
                "description": "Show applications dependencies.",
            },
            {
                "name": "async_metrics_dependencies",
                "method": "GET",
                "path": "/async_metrics/system/dependencies",
                "description": "Show applications dependencies.",
            },
            {
                "name": "async_metrics_python",
                "method": "HEAD",
                "path": "/async_metrics/system/python",
                "description": "Show information about current python environment.",
            },
            {
                "name": "async_metrics_python",
                "method": "GET",
                "path": "/async_metrics/system/python",
                "description": "Show information about current python environment.",
            },
            {
                "name": "async_metrics_process",
                "method": "HEAD",
                "path": "/async_metrics/system/process",
                "description": "Show summary information about application process.             ",
            },
            {
                "name": "async_metrics_process",
                "method": "GET",
                "path": "/async_metrics/system/process",
                "description": "Show summary information about application process.",
            },
            {
                "name": "async_metrics_partitions",
                "method": "HEAD",
                "path": "/async_metrics/system/partitions",
                "description": "Show summary information about disk partition.             ",
            },
            {
                "name": "async_metrics_partitions",
                "method": "GET",
                "path": "/async_metrics/system/partitions",
                "description": "Show summary information about disk partition.",
            },
            {
                "name": "async_metrics_about",
                "method": "HEAD",
                "path": "/async_metrics/system/about",
                "description": "Show information about async_metrics.             ",
            },
            {
                "name": "async_metrics_about",
                "method": "GET",
                "path": "/async_metrics/system/about",
                "description": "Show information about async_metrics.",
            },
        ]
        resp = make_response(jsonify(routes), 200)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
