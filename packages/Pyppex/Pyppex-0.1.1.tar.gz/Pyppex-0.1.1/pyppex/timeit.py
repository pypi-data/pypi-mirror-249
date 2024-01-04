from typing import Callable
from functools import wraps
import time, os

from pyppex import timecode

def timeit(func:Callable) -> Callable:
    '''
    Decorator to print out the execution time.
    It displays the name of the function if it's applyied to any function but main.
    A function called main will display instead of the name of the function, the name of the directory
    where the script that the function "main" lies within is located.

    Example:
    --------
        >>> @timeit
        >>> def my_function():
        ...     time.sleep(1)
        >>> my_function()
        'my_function took 00:00:01.000 seconds'

        >>> @timeit
        >>> def main():
        ...     time.sleep(79.5):
        >>> main()
        'your_directory took 00:01:19.500 minutes'        
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # If the decorated function is called main, prints it's directory name
        if func.__name__=='main':
            func_dir = os.path.basename(os.path.abspath(func.__module__)[:-9])
            print(f'\033[1m{func_dir}\033[0m took \033[1m{timecode(end_time - start_time)}\033[0m')
        # Prints it's function name if the function has another name but main
        else:
            print(f'\033[1m{func.__name__}\033[0m took \033[1m{timecode(end_time - start_time)}\033[0m')
        return result
    return wrapper