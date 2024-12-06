# (c) Isaac Godman 2024

import time
from typing import Callable

class Time:
    """A static class supporting time operations.
    
    Keeps track of the delta time between calls (recommended once per frame), and has a system to call functions after some time delay.
    Also supports scaling the delta time by some factor."""

    dt: float = 0
    """Time between frames in seconds, multiplied by the timescale."""
    true_dt: float = 0
    """Time between frames in seconds."""
    
    _last_time: float = time.time()
    
    timescale: float = 1
    """The factor to scale the true delta time to get the scaled delta time, dt."""

    _delayed_funcs: list[tuple[float, ]] = []
    
    def __init__(self, timescale = 1) -> None:
        timescale = timescale
    
    def update():
        """Update the Time class.
        
        Calculate the delta time since last called, and update the delayed functions list."""

        time_now = time.time()
        Time.true_dt = time_now - Time._last_time
        Time._last_time = time_now

        Time.dt = Time.true_dt * Time.timescale

        for func in Time._delayed_funcs:
            func[0] -= Time.dt

            if func[0] <= 0:
                func[1](*func[2], **func[3])
            
                Time._delayed_funcs.remove(func)
    
    def add_delayed_func(delay: float, func: Callable, *args, **kwargs):
        """Call a function after some delay.
        
        Parameters:
        - delay (float): The delay after which to call the function.
        - func (Callable): The method to call after some delay.
        - *args: Any positional arguments passed to the function.
        - **kwargs: Any keyword arguments passed to the function."""

        Time._delayed_funcs.append([delay, func, args, kwargs])