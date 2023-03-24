from typing import Callable


def print_context(message: str) -> Callable:
    def decorator(f: Callable):
        def wrapped(*args, **kwargs):
            print(f"{message}:")
            result = f(*args, **kwargs)
            print()
            return result

        return wrapped

    return decorator
