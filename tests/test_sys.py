import async_metrics


def test_cpu_info():
    resp = async_metrics.sys.cpu_info()
    assert len(resp) == 3


def test_partitions():
    resp = async_metrics.sys.partitions()
    assert resp != []


def test_process():
    resp = async_metrics.sys.process()
    assert len(resp) == 10


def test_python():
    resp = async_metrics.sys.python()
    assert len(resp) == 5


def test_modules():
    resp = async_metrics.sys.modules()
    assert len(resp) != 0


def test_packages():
    resp = async_metrics.sys.packages()
    assert len(resp) != 0
