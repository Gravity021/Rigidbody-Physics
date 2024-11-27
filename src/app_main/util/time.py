# (c) Isaac Godman 2024

import time

class Time:
    dt: float = 0
    true_dt: float = 0
    
    _last_time: float = time.time()
    
    timescale: float = 1
    
    _delayed_funcs: list[tuple[float, ]] = []
    
    def __init__(self, timescale = 1) -> None:
        timescale = timescale
    
    def update():
        time_now = time.time()
        Time.true_dt = time_now - Time._last_time
        Time._last_time = time_now

        Time.dt = Time.true_dt * Time.timescale

        for func in Time._delayed_funcs:
            func[0] -= Time.dt

            if func[0] <= 0:
                func[1](*func[2], **func[3])
            
                Time._delayed_funcs.remove(func)
    
    def add_delayed_func(delay, func, *args, **kwargs):
        Time._delayed_funcs.append((delay, func, args, kwargs))