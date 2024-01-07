from functools import wraps
from typing import Callable, Dict, Union, Any, Optional

PON_TIMER_METHOD_ATTR_NAME = 'pon_timer_func_config'


def timer(
    interval: Union[int, float],
    execute_before_sleep: bool = False,
    timeout: Optional[float] = None,
    wait: bool = True
):
    """

    Timer decorator for controlling execution and sleep intervals.

    TIPS: Every time you call a modifier modified function, the modifier class is instantiated

    Args:
        interval (Union[int, float]): Time interval for the timer.
        execute_before_sleep (bool, optional): Determines whether to execute before sleep. Defaults to False.
        timeout (float, optional): Timeout duration for the timer. Defaults to None.
        wait (bool, optional): Whether to wait for the timer. Defaults to True.

    Returns:
        Callable: Decorator function.

    Usage:
        @timer(interval=5, execute_before_sleep=True)
        def my_timer_function():
            # Function logic here

    """
    def decorate(pon_service_cls_timer_method: Callable):
        """
        Decorator function to configure and attach timer settings to a method.

        Args:
            pon_service_cls_timer_method (Callable): Method to be decorated.

        Returns:
            Callable: Decorated method.
        """
        pon_timer_func_config: Dict[str, Any] = {
            'interval': interval,
            'execute_before_sleep': execute_before_sleep,
            'timeout': timeout,
            'wait': wait,
        }

        if not hasattr(pon_service_cls_timer_method, PON_TIMER_METHOD_ATTR_NAME):
            setattr(
                pon_service_cls_timer_method,
                PON_TIMER_METHOD_ATTR_NAME,
                pon_timer_func_config
            )

        @wraps(pon_service_cls_timer_method)
        def wrapper(*args, **kwargs):
            return pon_service_cls_timer_method(*args, **kwargs)
        return wrapper
    return decorate
