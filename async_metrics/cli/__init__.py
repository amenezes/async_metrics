import click
import requests
from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from async_metrics import __version__

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)
console = Console()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument(
    "address",
    envvar="ASYNC_METRICS_HOST",
    default="http://localhost:8080/async_metrics",
)
@click.option(
    "--asyncio",
    is_flag=True,
    help="Show summary information about async environmen.",
)
@click.option(
    "--system",
    is_flag=True,
    help="Show information about system environment.",
)
@click.option(
    "--deps",
    is_flag=True,
    help="Show applications dependencies.",
)
@click.option(
    "--python",
    is_flag=True,
    help="Show information about current python environment.",
)
@click.option(
    "--process",
    is_flag=True,
    help="Show summary information about application process.",
)
@click.option(
    "--partitions",
    is_flag=True,
    help="Show summary information about disk partition.",
)
@click.option(
    "--about",
    is_flag=True,
    help="Show information about async_metrics.",
)
def show(address, asyncio, system, deps, python, process, partitions, about):
    table = Table.grid(padding=(0, 1))

    try:
        if asyncio:
            _print_asyncio(table, address)
        elif system:
            _print_system(table, address)
        elif deps:
            _print_deps(table, address)
        elif python:
            _print_python(table, address)
        elif process:
            _print_process(table, address)
        elif partitions:
            _print_partitions(table, address)
        elif about:
            _print_about(table, address)

        console.print(
            Panel(
                table,
                title="[bold yellow]async_metrics[/bold yellow]",
                border_style="yellow",
                expand=True,
            )
        )
    except Exception as err:
        console.log(f"[red][>][/red] Failed to contact server, due: {str(err)}")


def _print_asyncio(table, address):
    target_address = f"{address}/asyncio"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")
    table.add_column(style="yellow")
    for loop in json_data["asyncio"]["loop"]:
        table.add_row(
            "loop",
            f"running={loop['running']}",
            f"{loop['policy']}",
            f"{loop['exception_handler']}",
        )
    table.add_row("tasks_number ", str(json_data["asyncio"]["tasks_number"]))
    for task in json_data["asyncio"]["tasks"]:
        table.add_row("task", f"{task['id']}", f"{task['task_name']}")


def _print_system(table, address):
    target_address = f"{address}/system"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("uptime", json_data["system"]["summary"]["uptime"])
    table.add_row("platform", json_data["system"]["summary"]["platform"])
    table.add_row(
        "recursion_limit", str(json_data["system"]["summary"]["recursion_limit"])
    )
    table.add_row(
        "default_encoding", json_data["system"]["summary"]["default_encoding"]
    )
    table.add_row()
    table.add_row(
        "processors core",
        str(json_data["system"]["summary"]["cpu_info"]["processors"]["core"]),
    )
    table.add_row(
        "processors virtual",
        str(json_data["system"]["summary"]["cpu_info"]["processors"]["virtual"]),
    )
    table.add_row()
    table.add_row(
        "load last minute",
        str(json_data["system"]["summary"]["cpu_info"]["load_avg"][0]),
    )
    table.add_row(
        "load last 5 minutes",
        str(json_data["system"]["summary"]["cpu_info"]["load_avg"][1]),
    )
    table.add_row(
        "load last 15 minutes",
        str(json_data["system"]["summary"]["cpu_info"]["load_avg"][2]),
    )
    table.add_row()
    table.add_row("process user", str(json_data["system"]["summary"]["user"]["login"]))
    table.add_row("uid", str(json_data["system"]["summary"]["user"]["uid"]))
    table.add_row("gid", str(json_data["system"]["summary"]["user"]["gid"]))


def _print_deps(table, address):
    target_address = f"{address}/system/dependencies"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column()
    table.add_column(style="magenta")
    table.add_column()
    table.add_column(style="white")

    for package in json_data["packages"]:
        table.add_row(
            package["name"],
            "  ",
            package["version"],
            "  ",
            f"{package['dependencies']}",
        )


def _print_python(table, address):
    target_address = f"{address}/system/python"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row(
        json_data["implementation"],
        json_data["version"],
    )
    table.add_row("Path" "")
    for p in json_data["path"]:
        table.add_row("", p)


def _print_process(table, address):
    target_address = f"{address}/system/process"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("name ", json_data["name"])
    table.add_row("threads ", str(json_data["threads"]))
    table.add_row("open_files ", str(json_data["open_files"]))
    table.add_row("connections ", str(json_data["connections"]))
    table.add_row(
        "context_switch ",
        f"{json_data['context_switch']['voluntary']} {json_data['context_switch']['involuntary']}",
    )
    table.add_row("childrens PID ", str(json_data["childrens"]))


def _print_partitions(table, address):
    target_address = f"{address}/system/partitions"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("partition", "usage")
    for partition in json_data:
        for k, v in partition.items():
            table.add_row(k, f"{v}%")


def _print_about(table, address):
    target_address = f"{address}/about"
    console.log(f"async_metrics host: {target_address}")
    json_data = requests.get(target_address).json()

    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("version ", json_data["async_metrics_version"])
    table.add_row("project_url ", json_data["project_url"])
    table.add_row("issues ", json_data["issues"])
    table.add_row(
        "releases ",
        "https://github.com/amenezes/async_metrics/releases",
    )


def _no_data(table):
    table.add_column(style="cyan", justify="right")
    table.add_row("no data")
