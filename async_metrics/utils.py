import time
from functools import wraps


def measure_time_elapsed(fnc, **kwargs):
    @wraps(fnc)
    def _measure_it():
        start_time = time.perf_counter()
        resp = fnc.__call__()
        try:
            resp.update({"time_elapsed": time.perf_counter() - start_time})
        except AttributeError:
            resp = {
                fnc.__name__: resp,
                "time_elapsed": time.perf_counter() - start_time,
            }
        return resp

    return _measure_it
