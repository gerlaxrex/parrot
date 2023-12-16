# pylint: disable=C0103
"""A utility module for iterable containers"""
import itertools
import typing


T = typing.TypeVar("T")


def pairwise(S: typing.Iterable[T]) -> typing.Iterable[tuple[T, T]]:
    """It pairwise aggregates iterable elements

    .. math::
        S \longmapsto (s_0, s_1), (s_1, s_2), \ldots, (s_{n - 1}, s_n)
    """
    A, B = itertools.tee(S, 2)

    next(B, None)
    return zip(A, B)
