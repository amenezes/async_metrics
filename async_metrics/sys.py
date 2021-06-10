import os
import platform
import sys
from datetime import datetime
from operator import itemgetter

import pkg_resources
import psutil

from async_metrics.utils import measure_time_elapsed


@measure_time_elapsed
def summary():
    return {
        "uptime": uptime(),
        "platform": platform.platform(),
        "architecture": " ".join(list(platform.architecture())),
        "system": platform.system(),
        "recursion_limit": os.sys.getrecursionlimit(),
        "defualt_encoding": os.sys.getdefaultencoding(),
        "cpu_info": cpu_info(),
        "user": user_info(),
    }


def user_info() -> dict:
    try:
        return {
            "login": os.getlogin(),
            "uid": os.getuid(),
            "gid": os.getgid(),
            "groups": os.getgroups(),
        }
    except OSError:
        return {}


def uptime():
    uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    return uptime[: uptime.rfind(":")]


def cpu_info():
    return {
        "processors": {
            "virtual": os.cpu_count(),
            "core": psutil.cpu_count(logical=False),
        },
        "architecture": platform.processor(),
        "load_avg": list(os.getloadavg()),
    }


def modules():
    """modules loaded."""
    return list(os.sys.modules.keys())


@measure_time_elapsed
def packages():
    def package_info():
        for package in pkg_resources.working_set:
            name = package.project_name
            dependencies = [
                dependency.project_name for dependency in package.requires()
            ]
            lines = package.get_metadata_lines(package.PKG_INFO)
            url = "#"
            for line in lines:
                if line.startswith("Home-page:"):
                    url = line[10:].strip()
                    break
            yield {
                "version": package.version,
                "name": name,
                "dependencies": dependencies,
                "url": url,
            }

    return sorted([package for package in package_info()], key=itemgetter("name"))


def thread_info():
    return os.sys.thread_info


@measure_time_elapsed
def python():
    """Show information about current python environment."""
    return {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "path": sys.path,
        "api_version": sys.api_version,
    }


@measure_time_elapsed
def all():
    return {
        "summary": summary(),
        "partitions": partitions(),
        "processs": process(),
        "thread_info": thread_info(),
        "python": python(),
        "dependencies": packages(),
    }


def partitions():
    resp = []
    for partition in psutil.disk_partitions():
        resp.append(
            {partition.mountpoint: psutil.disk_usage(partition.mountpoint).percent}
        )
    return resp


@measure_time_elapsed
def process(process_id: int = os.getpid()):
    """Show information about current process."""
    pid = psutil.Process(process_id)
    return {
        "PID": pid.pid,
        "name": pid.name(),
        "cpu_info_percent": pid.cpu_percent(),
        "cpu_info_affinity": pid.cpu_affinity(),
        "threads": pid.num_threads(),
        "open_files": len(pid.open_files()),
        "filedescriptors": pid.num_fds(),
        "connections": len(pid.connections()),
        "context_switch": {
            "voluntary": pid.num_ctx_switches().voluntary,
            "involuntary": pid.num_ctx_switches().involuntary,
        },
        "childrens": [
            {
                cpid.pid: {
                    "name": cpid.name(),
                    "cmdline": cpid.cmdline(),
                }
            }
            for cpid in pid.children(recursive=True)
        ],
    }
