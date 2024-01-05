"""
"""

import typing

import numpy as np

from ._typedef import (
    RealFunction, RealNFunction
)



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
    def __init__(self, f: )
