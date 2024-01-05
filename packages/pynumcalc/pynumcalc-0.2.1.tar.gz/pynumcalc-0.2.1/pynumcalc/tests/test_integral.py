"""
Unit tests for :py:mod:`pynumcalc.integral`.
"""

import typing

import pytest

from pynumcalc import integral


@pytest.mark.parametrize(
    ("lower", "upper", "npartitions"), [
        (0, 0, 1), (0, 0, 2), (0, 0, 4), (0, 0, 8), (0, 0, 16),
        (0, 1, 1), (0, 2, 1), (0, 4, 1), (0, 8, 1), (0, 16, 1),
        (-1, 0, 1), (-2, 0, 1), (-4, 0, 1), (-8, 0, 1), (-16, 0, 1),
        (-1, 1, 1), (-2, 2, 1), (-4, 4, 1), (-8, 8, 1), (-16, 16, 1),
        (-1, 1, 2), (-1, 1, 2), (-1, 1, 4), (-1, 1, 8), (-1, 1, 16)
    ]
)
class TestPartitions:
    """
    Unit tests for :py:class:`integral.Partitions`.
    """
    def test_left(self, lower: float, upper: float, npartitions: int):
        """
        Unit test for :py:meth:`integral.Partitions.left`.
        """
        array = integral.Partitions.left(lower, upper, npartitions)

        assert array.size == npartitions
        assert array[0] == lower
        assert array[-1] == upper - (upper - lower) / npartitions

    def test_middle(self, lower: float, upper: float, npartitions: int):
        """
        Unit test for :py:meth:`integral.Partitions.middle`.
        """
        array = integral.Partitions.middle(lower, upper, npartitions)

        assert array.size == npartitions
        assert array[0] == lower + (upper - lower) / (2 * npartitions)
        assert array[-1] == upper - (upper - lower) / (2 * npartitions)

    def test_right(self, lower: float, upper: float, npartitions: int):
        """
        Unit test for :py:meth:`integral.Partitions.right`.
        """
        array = integral.Partitions.right(lower, upper, npartitions)

        assert array.size == npartitions
        assert array[0] == lower + (upper - lower) / npartitions
        assert array[-1] == upper


class TestRiemannSum:
    """
    Unit tests for :py:class:`integral.RiemannSum`.
    """
    @pytest.mark.parametrize(
        ("intervals", "expected"), [
            ([(0, 0, 1)], 0),
            ([(0, 0, 1), (0, 0, 1)], 0),
            ([(0, 0, 1), (0, 0, 1), (0, 0, 1)], 0),

            ([(0, 1, 1)], 1),
            ([(0, 1, 1), (0, 1, 1)], 1),
            ([(0, 1, 1), (0, 1, 1), (0, 1, 1)], 1),

            ([(0, 1, 5)], 1/5),
            ([(0, 1, 5), (0, 1, 5)], 1/25),
            ([(0, 1, 5), (0, 1, 5), (0, 1, 5)], 1/125),

            ([(1, 2, 4)], 1/4),
            ([(1, 2, 4), (8, 16, 32)], 1/16),
            ([(1, 2, 4), (8, 16, 32), (64, 128, 256)], 1/64),

            ([(1, 2, 3)], 1/3),
            ([(1, 2, 3), (4, 5, 6)], 1/18),
            ([(1, 2, 3), (4, 5, 6), (7, 8, 9)], 1/162),

            ([(1, 2, 3)], 1/3),
            ([(1, 2, 3), (5, 8, 13)], 1/13),
            ([(1, 2, 3), (5, 8, 13), (21, 34, 55)], 1/55),

            ([(-1, 1, 5)], 2/5),
            ([(-1, 1, 5), (-2, 2, 25)], 8/125),
            ([(-1, 1, 5), (-2, 2, 25), (-3, 3, 125)], 48/15625)
        ]
    )
    def test_delta(
        self, intervals: typing.Sequence[typing.Tuple[float, float, int]], expected: float
    ):
        """
        Unit test for :py:meth:`Integrate.delta`.
        """
        assert integral.RiemannSum.delta(*intervals) == expected

    @pytest.mark.parametrize(
        ("function", "intervals", "expected"), [
            (lambda _: 0, [(0, 0, 1)], (0, 0, 0)),
            (lambda _: 0, [(0, 1, 1)], (0, 0, 0)),
            (lambda _: 0, [(-1, 0, 1)], (0, 0, 0)),
            (lambda _: 0, [(-1, 1, 1)], (0, 0, 0)),
            (lambda _: 1, [(0, 0, 1)], (0, 0, 0)),

            (lambda _: 1, [(0, 1, 1)], (1, 1, 1)),
            (lambda _: 1, [(-1, 0, 1)], (1, 1, 1)),
            (lambda _: -1, [(0, 0, 1)], (0, 0, 0)),
            (lambda _: -1, [(0, 1, 1)], (-1, -1, -1)),
            (lambda _: -1, [(-1, 0, 1)], (-1, -1, -1)),

            (lambda x: x[0], [(0, 8, 32)], (31, 32, 33)),
            (lambda x: -x[0], [(0, 8, 32)], (-31, -32, -33)),
            (lambda x: x[0] ** 2, [(0, 8, 32)], (651/4, 1365/8, 715/4)),
            (lambda x: x[0] ** 3, [(0, 8, 32)], (961, 2047/2, 1089)),
            (lambda x: -x[0] ** 3, [(0, 8, 32)], (-961, -2047/2, -1089)),

            (lambda x: x[0] + x[1], [(0, 8, 2), (0, 8, 2)], (256, 512, 768)),
            (lambda x: x[0] + x[1], [(0, 8, 4), (0, 8, 4)], (384, 512, 640)),
            (lambda x: x[0] + x[1], [(0, 8, 8), (0, 8, 8)], (448, 512, 576)),
            (lambda x: x[0] + x[1], [(0, 8, 16), (0, 8, 16)], (480, 512, 544)),
            (lambda x: x[0] + x[1], [(0, 8, 32), (0, 8, 32)], (496, 512, 528)),

            (lambda x: x[0] * x[1], [(-8, 0, 2), (-8, 0, 2)], (2304, 1024, 256)),
            (lambda x: x[0] * x[1], [(-8, 0, 4), (-8, 0, 4)], (1600, 1024, 576)),
            (lambda x: x[0] * x[1], [(-8, 0, 8), (-8, 0, 8)], (1296, 1024, 784)),
            (lambda x: x[0] * x[1], [(-8, 0, 16), (-8, 0, 16)], (1156, 1024, 900)),
            (lambda x: x[0] * x[1], [(-8, 0, 32), (-8, 0, 32)], (1089, 1024, 961)),

            (lambda x: x[0] ** 2 + x[0] ** 2, [(-4, 4, 2), (-4, 4, 2)], (1024, 512, 1024)),
            (lambda x: x[0] ** 2 + x[1] ** 2, [(-4, 4, 4), (-4, 4, 4)], (768, 640, 768)),
            (lambda x: x[0] ** 2 + x[1] ** 2, [(-4, 4, 8), (-4, 4, 8)], (704, 672, 704)),
            (lambda x: x[0] ** 2 + x[1] ** 2, [(-4, 4, 16), (-4, 4, 16)], (688, 680, 688)),
            (lambda x: x[0] ** 2 + x[1] ** 2, [(-4, 4, 32), (-4, 4, 32)], (684, 682, 684)),
            
            (lambda x: (x[0] * x[1]) ** 2, [(-1, 1, 64), (-16, 16, 4)], (2049, 6825/4, 2049)),
            (lambda x: (x[0] * x[1]) ** 2, [(-2, 2, 32), (-8, 8, 8)], (1881, 7161/4, 1881)),
            (lambda x: (x[0] * x[1]) ** 2, [(-4, 4, 16), (-4, 4, 16)], (1849, 7225/4, 1849)),
            (lambda x: (x[0] * x[1]) ** 2, [(-8, 8, 8), (-2, 2, 32)], (1881, 7161/4, 1881)),
            (lambda x: (x[0] * x[1]) ** 2, [(-16, 16, 4), (-1, 1, 64)], (2049, 6825/4, 2049)),
        ]
    )
    def test_riemann_sum(
        self,
        function: typing.Callable[[typing.Sequence], float],
        intervals: typing.Sequence[typing.Tuple[float, float, int]],
        expected: typing.Tuple[float, float, float]
    ):
        """
        Unit test for :py:meth:`Integrate.riemann_sum`.
        """
        axes = (
            [integral.Partitions.left(*x) for x in intervals],
            [integral.Partitions.middle(*x) for x in intervals],
            [integral.Partitions.right(*x) for x in intervals]
        )
        delta = integral.RiemannSum.delta(*intervals)
        rsums = tuple(integral.RiemannSum.sum(function, a, delta) for a in axes)

        assert rsums == expected
