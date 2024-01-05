"""
"""

import functools
import itertools
import operator
import typing

import numpy as np


class Partitions:
    """
    """
    @classmethod
    def left(
        cls, lower: float, upper: float, npartitions: int
    ) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        r"""
        .. math::

            x_{i}^{*} = x_{i-1} = a + i \Delta x

        :param lower: The lower bound of the summation interval
        :param upper: The upper bound of the summation interval
        :param npartitions: The number of partitions dividing the interval
        :return:
        :raise ValueError:
        """
        if not (npartitions > 0 and isinstance(npartitions, int)):
            raise ValueError("parameter 'npartitions' must be a positive integer")

        length = (upper - lower) / npartitions
        return lower + np.arange(npartitions) * length

    @classmethod
    def right(
        cls, lower: float, upper: float, npartitions: int
    ) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        r"""
        .. math::

            x_{i}^{*} = x_{i} = a + (i + 1) \Delta x

        :param lower: The lower bound of the summation interval
        :param upper: The upper bound of the summation interval
        :param npartitions: The number of partitions dividing the interval
        :return:
        :raise ValueError:
        """
        if not (npartitions > 0 and isinstance(npartitions, int)):
            raise ValueError("parameter 'npartitions' must be a positive integer")

        length = (upper - lower) / npartitions
        return lower + (np.arange(npartitions) + 1) * length

    @classmethod
    def middle(
        cls, lower: float, upper: float, npartitions: int
    ) -> np.ndarray[typing.Any, np.dtype[np.float64]]:
        r"""
        .. math::

            x_{i}^{*} = \frac{x_{i-1} + x_{i}}{2} = a + (i + \frac{1}{2}) \Delta x

        :param lower: The lower bound of the summation interval
        :param upper: The upper bound of the summation interval
        :param npartitions: The number of partitions dividing the interval
        :return:
        :raise ValueError:
        """
        if not (npartitions > 0 and isinstance(npartitions, int)):
            raise ValueError("parameter 'npartitions' must be a positive integer")

        length = (upper - lower) / npartitions
        return lower + (np.arange(npartitions) + 1 / 2) * length


class RiemannSum:
    """
    """
    @classmethod
    def delta(cls, *intervals: typing.Tuple[float, float, int]) -> float:
        """
        :param axes:
        :return:
        """
        return functools.reduce(
            operator.mul, (b - a for a, b, _ in intervals)
        ) / functools.reduce(
            operator.mul, (n for _, _, n in intervals)
        )
    
    @classmethod
    def sum(
        cls, function: typing.Callable[[typing.Sequence], float],
        axes: typing.Sequence[np.ndarray[typing.Any, np.dtype[np.float64]]], delta: float
    ) -> float:
        """
        :param function:
        :param axes:
        :param delta:
        :return:
        """
        return sum(map(function, itertools.product(*axes))) * delta


def integrate(
    f: typing.Callable[[typing.Sequence[float]], float],
    *intervals: typing.Tuple[float, float, int]
) -> float:
    """
    :param function:
    :param intervals:
    :return:
    """
    dimensions = np.array(
        [[Partitions.left(*x), Partitions.right(*x)] for x in intervals]
    )

    return sum(
        RiemannSum.sum(
            f, np.array([a[i] for a, i in zip(dimensions, indices)]), RiemannSum.delta(*intervals)
        ) for indices in itertools.product((0, 1), repeat=len(intervals))
    ) / pow(2, len(intervals))
