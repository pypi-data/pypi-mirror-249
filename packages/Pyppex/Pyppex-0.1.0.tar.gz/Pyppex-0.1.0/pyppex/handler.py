from typing import Callable
from functools import wraps
import pyppex as px
import logging


def handler(logger:logging=None):
    def decorator(func:Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            
            except Exception as e:
                if logger:
                    logger.error(e, exc_info=True)
                else:
                    print(px.modstring(e, mod='red'))
            
        return wrapper
    return decorator
