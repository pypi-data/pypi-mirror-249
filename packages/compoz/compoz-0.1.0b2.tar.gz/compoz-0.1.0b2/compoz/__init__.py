"""Provides with composition tools.
"""
from typing import Iterable, Reversible, Callable
from functools import reduce

__all__ = [
    "composite",
    "pipe",
]


def composite(funcs: Iterable[Callable]) -> Callable:
    """Provides with functional composition.

    :param funcs: A list of callables that will be executed from last to first when called.
    :return: A composite function.
    """
    return reduce(_compose, funcs)


def pipe(funcs: Reversible[Callable]) -> Callable:
    """Provides with piped functional composition.

    :param funcs: A list of callables that will be executed from first to last when called.
    :return: A piped composite function.
    """
    return reduce(_compose, reversed(funcs))


def _compose(g, f) -> Callable:  # pylint: disable=invalid-name
    """Provides with a composite function where the result of f will be passed to g.
    """
    def h(*args, **kwargs):  # pylint: disable=invalid-name
        return g(f(*args, **kwargs), **kwargs)

    return h
