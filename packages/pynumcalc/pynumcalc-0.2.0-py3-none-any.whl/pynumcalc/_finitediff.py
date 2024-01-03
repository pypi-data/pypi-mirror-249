"""
"""

import typing

import numpy as np
import scipy.special

from ._typedef import (
    RealFunction, RealNFunction
)


class FiniteDifference:
    r"""
    Computes finite differences for a one-dimensional real-valued function ``f``,
    :math:`f: \mathbb{R} \mapsto \mathbb{R}`, using step size ``h``.
    """
    def __init__(self, f: RealFunction, h: float):
        self._f = f
        self._h = h

    @staticmethod
    def _first(f: RealFunction, h: float, x: float) -> float:
        raise NotImplementedError
    
    @staticmethod
    def _second(f: RealFunction, h: float, x: float) -> float:
        raise NotImplementedError
    
    @staticmethod
    def _nth(f: RealFunction, h: float, x: float, n: int) -> float:
        raise NotImplementedError
    
    @property
    def f(self) -> RealFunction:
        r"""
        A one-dimension real-valued function, :math:`f: \mathbb{R} \mapsto \mathbb{R}`.
        """
        return self._f
    
    @property
    def h(self) -> float:
        """
        The step size used to compute finite differences.
        """
        return self._h
    
    @h.setter
    def h(self, value: float) -> None:
        self._h = float(value)

    def first(self, x: float) -> float:
        """
        Computes the first-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        return self._first(self.f, self.h, x)
    
    def second(self, x: float) -> float:
        """
        Computes the second-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        return self._second(self.f, self.h, x)
    
    def nth(self, x: float, n: int) -> float:
        r"""
        Computes the ``n``\th-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        return self._nth(self.f, self.h, x, n)


class PFiniteDifference:
    r"""
    Computes finite differences for a :math:`n`-dimensional real-valued function ``f``,
    :math:`f: {\mathbb{R}}^{n} \mapsto \mathbb{R}`, of ``ndim`` dimensions using step size ``h``.
    """
    def __init__(self, f: RealNFunction, ndim: int, h: float):
        self._f = f
        self._ndim = ndim
        self._h = h

    @staticmethod
    def _first(f: RealFunction, dim: int, h: float, x: np.ndarray) -> float:
        raise NotImplementedError
    
    @staticmethod
    def _second(f: RealFunction, dim: int, h: float, x: np.ndarray) -> float:
        raise NotImplementedError
    
    @staticmethod
    def _nth(f: RealFunction, dim: int, h: float, x: np.ndarray, n: int) -> float:
        raise NotImplementedError
    
    @property
    def f(self) -> RealNFunction:
        r"""
        A :math:`n`-dimension real-valued function, :math:`f: {\mathbb{R}}^{n} \mapsto \mathbb{R}`,
        of :py:attr:`dim` dimensions.
        """
        return self._f
    
    @property
    def ndim(self) -> int:
        """
        The number of dimensions of the domain of :py:attr:`f`.
        """
        return self._ndim
    
    @property
    def h(self) -> float:
        """
        The step size used to compute finite differences.
        """
        return self._h
    
    @h.setter
    def h(self, value: float) -> None:
        self._h = float(value)

    @typing.overload
    def first(self, x: float) -> np.ndarray: ...

    @typing.overload
    def first(self, x: float, dim: int) -> float: ...

    def first(self, x: float, dim: int = None) -> typing.Union[np.ndarray, float]:
        """
        Computes the first-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        if dim is None:
            return np.array([self._first(self.f, d, self.h, x) for d in range(self.ndim)])
        return self._first(self.f, dim, self.h, x)
    
    @typing.overload
    def second(self, x: float) -> np.ndarray: ...

    @typing.overload
    def second(self, x: float, dim: int) -> float: ...

    def second(self, x: float, dim: int = None) -> np.ndarray:
        """
        Computes the second-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        if dim is None:
            return np.array([self._second(self.f, d, self.h, x) for d in range(self.ndim)])
        return self._second(self.f, dim, self.h, x)
    
    @typing.overload
    def nth(self, x: float, n: int) -> np.ndarray: ...

    @typing.overload
    def nth(self, x: float, n: int, dim: int) -> float: ...

    def nth(self, x: float, n: int, dim: int = None) -> typing.Union[np.ndarray, float]:
        r"""
        Computes the ``n``\th-order finite difference of :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        if dim is None:
            return np.array([self._nth(self.f, d, self.h, x, n) for d in range(self.ndim)])
        return self._nth(self.f, dim, self.h, x, n)


class Forward(FiniteDifference):
    r"""
    Computes :math:`n`th-order forward finite differences, :math:`{\Delta}_{h}^{n} [f](x)` for a
    one-dimensional real-valued function ``f``, :math:`f: \mathbb{R} \mapsto \mathbb{R}`, using
    step size ``h``.
    """
    @staticmethod
    def _first(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\Delta}_{h} [f](x) = f(x + h) - f(x)
        """
        return f(x + h) - f(x)
    
    @staticmethod
    def _second(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\Delta}_{h}^{2} [f](x) = f(x + 2h) - 2f(x + h) + f(x)
        """
        return f(x + 2 * h) - 2 * f(x + h) + f(x)
    
    @staticmethod
    def _nth(f: RealFunction, h: float, x: float, n: int) -> float:
        r"""
        .. math::

            {\Delta}_{h}^{n} [f](x) = \sum_{k=0}^{n} {(-1)}^{n-k} {{n}\choose{k}} f(x + kh)
        """
        array = np.arange(0, n + 1)
        return ((-1) ** (n - array) * scipy.special.comb(n, array) * f(x + array * h)).sum()


class Backward(FiniteDifference):
    r"""
    Computes :math:`n`th-order backward finite differences, :math:`{\nabla}_{h}^{n} [f](x)` for a
    one-dimensional real-valued function ``f``, :math:`f: \mathbb{R} \mapsto \mathbb{R}`, using
    step size ``h``.
    """
    @staticmethod
    def _first(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\nabla}_{h} [f](x) = f(x) - f(x - h)
        """
        return f(x) - f(x - h)
    
    @staticmethod
    def _second(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\nabla}_{h}^{2} [f](x) = f(x) - 2f(x - h) + f(x - 2h)
        """
        return f(x) - 2 * f(x - h) + f(x - 2 * h)
    
    @staticmethod
    def _nth(f: RealFunction, h: float, x: float, n: int) -> float:
        r"""
        .. math::

            {\nabla}_{h}^{n} [f](x) = \sum_{k=0}^{n} {(-1)}^{k} {{n}\choose{k}} f(x - kh)
        """
        array = np.arange(0, n + 1)
        return ((-1) ** array * scipy.special.comb(n, array) * f(x - array * h)).sum()


class Central(FiniteDifference):
    r"""
    Computes :math:`n`th-order central finite differences, :math:`{\delta}_{h}^{n} [f](x)` for a
    one-dimensional real-valued function ``f``, :math:`f: \mathbb{R} \mapsto \mathbb{R}`, using
    step size ``h``.
    """
    @staticmethod
    def _first(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\delta}_{h} [f](x) = f(x + \frac{h}{2}) - f(x - \frac{h}{2})
        """
        return f(x + h / 2) - f(x - h / 2)
    
    @staticmethod
    def _second(f: RealFunction, h: float, x: float) -> float:
        r"""
        .. math::

            {\delta}_{h}^{2} [f](x) = f(x + h) - 2f(x) + f(x - h)
        """
        return f(x + h) - 2 * f(x) + f(x - h)
    
    @staticmethod
    def _nth(f: RealFunction, h: float, x: float, n: int) -> float:
        r"""
        .. math::

            {\delta}_{h}^{n} [f](x) = \sum_{k=0}^{n} {(-1)}^{k} {{n}\choose{k}} f(x + (\frac{n}{2} - k)h)
        """
        array = np.arange(0, n + 1)
        return ((-1) ** array * scipy.special.comb(n, array) * f(x + (n / 2 - array) * h)).sum()


class PForward(PFiniteDifference):
    r"""
    Computes :math:`n`th-order forward finite differences, :math:`{\Delta}_{h}^{n} [f](\vec{x})`
    for a :math:`n`-dimensional real-valued function ``f``,
    :math:`f: \mathbb{R} \mapsto \mathbb{R}`, of ``dim`` dimensions using step size ``h``.

    .. math::

        {\Delta}_{h} [f](\vec{x}) = \begin{bmatrix}
            {\Delta}_{h} {[f]}_{x_1}(\vec{x}) \\
            \vdots \\
            {\Delta}_{h} {[f]}_{x_{\dim{\vec{x}}}}(\vec{x}) \\
        \end{bmatrix}
    """
    @staticmethod
    def _first(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\Delta}_{h} {[f]}_{x_i}(\vec{x}) = f(
                \langle x_1, \dots, x_i + h, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) - f(\vec{x})
        """
        return f([*x[:dim], x[dim] + h, *x[(dim + 1):]]) - f(x)
    
    @staticmethod
    def _second(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\Delta}_{h}^{2} {[f]}_{x_i}(\vec{x}) = f(
                \langle x_1, \dots, x_i + 2h, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) - 2f(
                \langle x_1, \dots, x_i + h, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) + f(\vec{x})
        """
        return f(
            [*x[:dim], x[dim] + 2 * h, *x[(dim + 1):]]
        ) - 2 * f(
            [*x[:dim], x[dim] + h, *x[(dim + 1):]]
        ) + f(x)

    @staticmethod
    def _nth(f: RealNFunction, dim: int, h: float, x: np.ndarray, n: int) -> float:
        r"""
        .. math::

            {\Delta}_{h}^{n} {[f]}_{x_i}(\vec{x}) = \sum_{k=0}^{n} {(-1)}^{n-k} {{n}\choose{k}} f(
                \langle x_1, \dots, x_i + kh, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        array = np.arange(0, n + 1)
        return (
            (-1) ** (n - array) * scipy.special.comb(n, array) * f(
                [*x[:dim], x[dim] + array * h, *x[(dim + 1):]]
            )
        ).sum()


class PBackward(PFiniteDifference):
    r"""
    Computes :math:`n`th-order backward finite differences, :math:`{\nabla}_{h}^{n} [f](\vec{x})`
    for a :math:`n`-dimensional real-valued function ``f``,
    :math:`f: \mathbb{R} \mapsto \mathbb{R}`, of ``dim`` dimensions using step size ``h``.

    .. math::

        {\nabla}_{h} [f](\vec{x}) = \begin{bmatrix}
            {\nabla}_{h} {[f]}_{x_1}(\vec{x}) \\
            \vdots \\
            {\nabla}_{h} {[f]}_{x_{\dim{\vec{x}}}}(\vec{x}) \\
        \end{bmatrix}
    """
    @staticmethod
    def _first(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\nabla}_{h} {[f]}_{x_i}(\vec{x}) = f(\vec{x}) - f(
                \langle x_1, \dots, x_i - h, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        return f(x) - f([*x[:dim], x[dim] - h, *x[(dim + 1):]])
    
    @staticmethod
    def _second(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\nabla}_{h}^{2} {[f]}_{x_i}(\vec{x}) = f(\vec{x}) - 2f(
                \langle x_1, \dots, x_i - h, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) + f(
                \langle x_1, \dots, x_i - 2h, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        return f(x) - 2 * f(
            [*x[:dim], x[dim] - h, *x[(dim + 1):]]
        ) + f(
            [*x[:dim], x[dim] - 2 * h, *x[(dim + 1):]]
        )
    
    @staticmethod
    def _nth(f: RealNFunction, dim: int, h: float, x: np.ndarray, n: int) -> float:
        r"""
        .. math::

            {\nabla}_{h}^{n} {[f]}_{x_i}(\vec{x}) = \sum_{k=0}^{n} {(-1)}^{k} {{n}\choose{k}} f(
                \langle x_1, \dots, x_i - kh, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        array = np.arange(0, n + 1)
        return (
            (-1) ** array * scipy.special.comb(n, array) * f(
                [*x[:dim], x[dim] - array * h, *x[(dim + 1):]]
            )
        ).sum()


class PCentral(PFiniteDifference):
    r"""
    Computes :math:`n`th-order forward finite differences, :math:`{\delta}_{h}^{n} [f](\vec{x})`
    for a :math:`n`-dimensional real-valued function ``f``,
    :math:`f: \mathbb{R} \mapsto \mathbb{R}`, of ``dim`` dimensions using step size ``h``.

    .. math::

        {\delta}_{h} [f](\vec{x}) = \begin{bmatrix}
            {\delta}_{h} {[f]}_{x_1}(\vec{x}) \\
            \vdots \\
            {\delta}_{h} {[f]}_{x_{\dim{\vec{x}}}}(\vec{x}) \\
        \end{bmatrix}
    """
    @staticmethod
    def _first(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\delta}_{h} {[f]}_{x_i}(\vec{x}) = f(
                \langle x_1, \dots, x_i + \frac{h}{2}, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) - f(
                \langle x_1, \dots, x_i - \frac{h}{2}, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        return f(
            [*x[:dim], x[dim] + h / 2, *x[(dim + 1):]]
        ) - f(
            [*x[:dim], x[dim] - h / 2, *x[(dim + 1):]]
        )
    
    @staticmethod
    def _second(f: RealNFunction, dim: int, h: float, x: np.ndarray) -> float:
        r"""
        .. math::

            {\delta}_{h}^{2} {[f]}_{x_i}(\vec{x}) = f(
                \langle x_1, \dots, x_i + h, \dots, {x}_{\dim{\vec{x}}} \rangle
            ) - 2f(\vec{x}) + f(
                \langle x_1, \dots, x_i - h, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        return f(
            [*x[:dim], x[dim] + h, *x[(dim + 1):]]
        ) - 2 * f(x) + f(
            [*x[:dim], x[dim] - h, *x[(dim + 1):]]
        )
    
    @staticmethod
    def _nth(f: RealNFunction, dim: int, h: float, x: np.ndarray, n: int) -> float:
        r"""
        .. math::

            {\delta}_{h}^{n} {[f]}_{x_i}(\vec{x}) = \sum_{k=0}^{n} {(-1)}^{k} {{n}\choose{k}} f(
                \langle x_1, \dots, x_i + (\frac{n}{2} - k)h, \dots, {x}_{\dim{\vec{x}}} \rangle
            )
        """
        array = np.arange(0, n + 1)
        return (
            (-1) ** array * scipy.special.comb(n, array) * f(
                [*x[:dim], x[dim] + (n / 2 - array) * h, *x[(dim + 1):]]
            )
        ).sum()
