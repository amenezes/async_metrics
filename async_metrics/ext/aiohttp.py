from aiohttp import web

import async_metrics
from async_metrics.ext.restrict_access import restrict_access


def setup_async_metrics(
    app: web.Application,
    subapp_name: str = "async_metrics",
):
    monitoring = web.Application(middlewares=[restrict_access])
    monitoring.add_routes(
        [
            web.get("/summary", _main_handler, name="async_metrics_summary"),
            web.get("/all", _metrics_handler, name="async_metrics_all"),
            web.get(
                "/asyncio",
                _asyncio_metrics_handler,
                name="async_metrics_asyncio",
            ),
            web.get(
                "/system",
                _system_metrics_handler,
                name="async_metrics_system",
            ),
            web.get(
                "/system/dependencies",
                _dependencies_metrics_handler,
                name="async_metrics_dependencies",
            ),
            web.get(
                "/system/python",
                _python_metrics_handler,
                name="async_metrics_python",
            ),
            web.get(
                "/system/process",
                _process_metrics_handler,
                name="async_metrics_process",
            ),
            web.get(
                "/system/partitions",
                _partitions_metrics_handler,
                name="async_metrics_partitions",
            ),
            web.get(
                "/routes",
                _routes_handler,
                name="async_metrics_routes",
            ),
            web.get("/about", _about_handler, name="async_metrics_about"),
        ]
    )
    app.add_subapp(f"/{subapp_name}", monitoring)
    app["async_metrics"] = monitoring


async def _main_handler(request: web.Request):
    """Show async_metrics available."""
    routes_path = request.app.router["async_metrics_routes"].url_for()
    url = f"{request.host}{routes_path}"
    body = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <title>aysnc_metrics</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.0/font/bootstrap-icons.css">
    </head>
    <body class="bg-light">
      <div class="container">
            <div class="d-flex flex-row-reverse bd-highlight">
                <div class="p-2 bd-highlight"><a class="nav-link active" aria-current="page" href="http://github.com/amenezes/async_metrics">
                    <button type="button" class="btn btn-link">GitHub</button>
                </a></div>
                <div class="p-2 bd-highlight"><a class="nav-link active" aria-current="page" href="http://github.com/amenezes/async_metrics/issues">
                    <button type="button" class="btn btn-link">Issues</button>
                </a></div>
            </div>
      </div>
       <div class="container">
            <div class="shadow-sm p-3 mb-5 bg-body rounded">
            <div class="d-flex p-2 bd-highlight">
                <h2 class="fs-3 fw-bolder">async_metrics <span class="badge bg-dark">{async_metrics.__version__}</span></h2>
            </div>
            <br />
            <div class="container">
                <div class="bd-callout bd-callout-info">
                    <h5 id="conveying-meaning-to-assistive-technologies"><p>Endpoints</p></h5>
                </div>
                <div class="table-responsive">
                    <table class="table table-striped"></table>
                </div>
            </div>
        </div>
      <script>
        async function start() {{
            let response = await fetch('http://{url}');
            let table = document.querySelector("table");
            let links = await response.json();

            for (let element of links) {{
                let row = table.insertRow();
                for (key in element) {{
                    let cell = row.insertCell();
                    let text = document.createTextNode(element[key]);
                    cell.appendChild(text);
                }}
            }}

            let thead = table.createTHead();
            let row = thead.insertRow();
            for (let key of Object.keys(links[0])) {{
                let th = document.createElement("th");
                let text = document.createTextNode(key);
                th.appendChild(text);
                row.appendChild(th);
            }}
        }}
        start();
      </script>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return web.Response(body=body, content_type="text/html")


async def _metrics_handler(request: web.Request):
    """Show information about async and system environment."""
    return web.json_response(
        {
            "asyncio": async_metrics.asyncio.all(),
            "system": async_metrics.sys.all(),
        }
    )


async def _asyncio_metrics_handler(request: web.Request):
    """Show summary information about async environment."""
    return web.json_response({"asyncio": async_metrics.asyncio.all()})


async def _system_metrics_handler(request: web.Request):
    """Show information about system environment."""
    return web.json_response({"system": async_metrics.sys.all()})


async def _python_metrics_handler(request: web.Request):
    """Show information about current python environment."""
    return web.json_response(async_metrics.sys.python())


async def _process_metrics_handler(request: web.Request):
    """Show summary information about application process."""
    return web.json_response(async_metrics.sys.process())


async def _partitions_metrics_handler(request: web.Request):
    """Show summary information about disk partition."""
    return web.json_response(async_metrics.sys.partitions())


async def _dependencies_metrics_handler(request: web.Request):
    """Show applications dependencies."""
    return web.json_response(async_metrics.sys.packages())


async def _routes_handler(request: web.Request):
    """Show async_metrics HTTP routes available."""
    return web.json_response(
        _routes(request), headers={"Access-Control-Allow-Origin": "*"}
    )


async def _about_handler(request: web.Request):
    """Show information about async_metrics."""
    return web.json_response(
        {
            "async_metrics_version": async_metrics.__version__,
            "project_url": "https://github.com/amenezes/async_metrics",
            "issues": "https://github.com/amenezes/async_metrics/issues",
        }
    )


def _routes(request):
    return [
        {
            "name": route.name or "",
            "method": route.method,
            "path": sorted(route.get_info().values()),
            "handler": route.handler.__doc__,
        }
        for route in request.app.router.routes()
    ]
