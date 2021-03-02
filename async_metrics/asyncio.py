import asyncio
import inspect
from typing import Dict, List

from async_metrics.utils import measure_time_elapsed


def loop_info() -> List[Dict]:
    """Show information about running loop."""
    loop = asyncio.get_event_loop()
    return [
        {
            "running": loop.is_running(),
            "policy": str(asyncio.get_event_loop_policy().__class__).split("'")[1],
            "exception_handler": loop.get_exception_handler(),
        }
    ]


def summary() -> Dict:
    try:
        return {
            "tasks": len(asyncio.all_tasks()),
            "watcher": asyncio.get_child_watcher().__doc__.split(".")[0],  # type: ignore
        }
    except RuntimeError:
        return {}


def current_task_info() -> Dict:
    try:
        ctask = asyncio.current_task()
        return _task_info(ctask)
    except (AttributeError, RuntimeError):
        return {}


def tasks_info() -> List[Dict]:
    try:
        return [_task_info(task) for task in asyncio.all_tasks()]
    except RuntimeError:
        return []


def _task_info(task) -> Dict:
    return {
        "id": id(task),
        "name": task.get_coro().__qualname__,
        "task_name": task.get_name(),
        "done": task.done(),
        "cancelled": task.cancelled(),
        "state": task._state,
        "details": {"locals": inspect.getcoroutinelocals(task)},
    }


@measure_time_elapsed
def all() -> Dict:
    return {
        "summary": summary(),
        "loop": loop_info(),
        "current_task": current_task_info(),
        "tasks": tasks_info(),
    }
