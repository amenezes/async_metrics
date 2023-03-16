import asyncio
import inspect
from typing import Dict, List

from async_metrics.utils import measure_time_elapsed


def loop_info() -> List[Dict]:
    """Show information about running loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            return [dict(running=False, policy=None, exception_handler=None)]
    return [
        {
            "running": loop.is_running(),
            "policy": str(asyncio.get_event_loop_policy().__class__).split("'")[1],
            "exception_handler": loop.get_exception_handler(),
        }
    ]


def current_task_info() -> Dict:
    try:
        ctask = asyncio.current_task()
        return _task_info(ctask)
    except (AttributeError, RuntimeError):
        return {}


def tasks_info() -> List[Dict]:
    resp = []
    try:
        resp = [_task_info(task) for task in asyncio.all_tasks()]
    except RuntimeError:
        pass
    return resp


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
    try:
        tasks_number = len(asyncio.all_tasks())
    except RuntimeError:
        tasks_number = 0
    return {
        "loop": loop_info(),
        "current_task": current_task_info(),
        "tasks_number": tasks_number,
        "tasks": tasks_info(),
    }
