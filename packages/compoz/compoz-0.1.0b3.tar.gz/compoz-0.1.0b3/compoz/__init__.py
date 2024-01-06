"""Provides with composition tools.
"""
from typing import Callable
from functools import reduce

__all__ = [
    "composite",
    "pipe",
]


def composite(*funcs) -> Callable:
    """Provides with functional composition.

    :param funcs: A series of callables that will be executed from last to first when called.
    :return: A composite function.
    """
    return reduce(_compose, funcs)


def pipe(*funcs) -> Callable:
    """Provides with piped functional composition.

    :param funcs: A series of callables that will be executed from first to last when called.
    :return: A piped composite function.
    """
    return reduce(_compose, reversed(funcs))


def _compose(g, f) -> Callable:  # pylint: disable=invalid-name
    """Provides with a composite function where the result of f will be passed to g.
    """
    def h(*args):  # pylint: disable=invalid-name
        return g(f(*args))

    return h
