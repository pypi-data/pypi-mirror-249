import functools
import traceback
from datetime import datetime
from time import sleep
from inspect import signature
from SmartApi.smartExceptions import DataException
from typing import Callable
from volstreet import config
from volstreet.config import logger, thread_local
from volstreet.utils import current_time, notifier
from volstreet.exceptions import APIFetchError


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = (datetime.now() - start).total_seconds()
        logger.info(f"Time taken for {func.__name__}: {end:.2f} seconds")
        return result

    return wrapper


def log_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            user_prefix = config.ERROR_NOTIFICATION_SETTINGS.get("user", "")
            logger.error(
                f"{user_prefix}Error in function {func.__name__}: {e}\nTraceback:{traceback.format_exc()}"
            )
            notifier(
                f"{user_prefix}Error in function {func.__name__}: {e}\nTraceback:{traceback.format_exc()}",
                config.ERROR_NOTIFICATION_SETTINGS["url"],
                "ERROR",
            )
            raise e

    return wrapper


def retry_angel_api(
    data_type: str | Callable = None,
    max_attempts: int = 10,
    wait_increase_factor: float = 1.5,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                sleep_duration = 1
                data = {}

                try:
                    data = func(*args, **kwargs)
                    # If data_type is a function that indexes into the data, call it
                    if callable(data_type):
                        return data_type(data)
                    if data_type == "ltp":
                        return data["data"]["ltp"]
                    else:
                        return data["data"]
                except Exception as e:
                    msg = f"Attempt {attempt}: Error in function {func.__name__}: {e}"
                    additional_msg = data.get(
                        "message", "No additional message available"
                    )

                    # Invalid book type error in fetch_book
                    if isinstance(e, ValueError) and "Invalid book type" in e.args[0]:
                        raise e

                    # Access rate error
                    elif (
                        isinstance(e, DataException)
                        and "exceeding access rate" in e.args[0]
                    ):
                        if attempt == max_attempts:
                            logger.error(
                                f"{msg}. Additional info from payload: {additional_msg}"
                            )
                            raise e

                        sleep_duration *= wait_increase_factor  # Exponential backoff

                    # Other errors
                    else:
                        if getattr(thread_local, "robust_handling", False):
                            if attempt == max_attempts:
                                logger.error(
                                    f"{msg}. Additional info from payload: {additional_msg}"
                                )
                                raise e

                            elif (
                                attempt == max_attempts - 2
                            ):  # Approaching max attempts
                                logger.info(
                                    f"Attempt {attempt} failed. Trying big sleep."
                                )
                                seconds_to_day_end: int = (
                                    datetime(
                                        *current_time().date().timetuple()[:3],
                                        hour=15,
                                        minute=29,
                                    )
                                    - current_time()
                                ).seconds

                                max_sleep = max(min(60, seconds_to_day_end // 2), 1)

                                sleep(max_sleep)
                                continue

                            sleep_duration *= (
                                wait_increase_factor  # Exponential backoff
                            )

                        elif attempt == 5:
                            logger.error(
                                f"{msg}. Additional info from payload: {additional_msg}"
                            )
                            raise APIFetchError(msg)

                    logger.info(
                        f"{msg}. Additional info from payload: {additional_msg}. "
                        f"Retrying in {sleep_duration} seconds."
                    )
                    sleep(sleep_duration)
                    continue

        return wrapper

    return decorator


def increase_robustness(func):
    """This decorator will set a flag in the thread local storage that will be used by the other functions in the same
    thread to increase robustness. Currently, it is used to increase the number of attempts in retry_angel_api
    decorator. But in the future, it can be used to increase robustness in other ways too (by other functions running
    in the same thread).
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Set the flag to True before calling the actual function
        thread_local.robust_handling = True
        try:
            result = func(*args, **kwargs)
        finally:
            # Ensure the flag is set back to False after the function ends
            thread_local.robust_handling = False
        return result

    return wrapper


class ClassProperty:
    def __init__(self, method):
        self.method = method

    def __get__(self, obj, cls):
        return self.method(cls)


def classproperty(func):
    return ClassProperty(func)


class SingletonInstances(type):
    _instances = {}

    # The __call__ determines what happens when instances of SingletonInstances are called
    # Instances of SingletonInstances are classes themselves. So, when they are called, they are actually being
    # instantiated.
    # calling super().__call__ will instantiate the class if it is new/unique and return the instance
    # calling SingletonInstances() actually invokes the class-method of 'type' class and not the __call__ below
    # which has the power to create new classes
    def __call__(cls, *args, **kwargs):
        if getattr(cls, "_disable_singleton", False):
            return super().__call__(*args, **kwargs)

        sig = signature(cls.__init__)
        bound = sig.bind_partial(cls, *args, **kwargs)
        bound.apply_defaults()

        # Skip the first argument ('self') and combine args and sorted kwargs values
        sorted_kwargs_values = tuple(value for _, value in sorted(bound.kwargs.items()))
        combined_args = tuple(bound.args[1:]) + sorted_kwargs_values
        key = (cls, combined_args)

        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        else:
            logger.debug(
                f"Reusing existing instance for {cls.__name__} with args {key}"
            )
        return cls._instances[key]

    @classproperty
    def instances(cls):
        return cls._instances
