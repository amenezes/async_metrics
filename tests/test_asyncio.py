import async_metrics


async def test_tasks_info():
    resp = async_metrics.asyncio.tasks_info()
    assert len(resp) == 1


def test_tasks_info_without_event_loop():
    resp = async_metrics.asyncio.tasks_info()
    assert resp == []


async def test_loop_info():
    resp = async_metrics.asyncio.loop_info()
    assert resp is not None


def test_loop_info_without_event_loop():
    resp = async_metrics.asyncio.loop_info()
    assert resp is not None


async def test_current_task_info():
    resp = async_metrics.asyncio.current_task_info()
    assert resp is not None


def test_current_task_info_without_event_loop():
    resp = async_metrics.asyncio.current_task_info()
    assert resp == {}
