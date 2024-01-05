"""
"""

import numpy as np

from ._finitediff import (
    Forward, Backward, Central, PForward, PBackward, PCentral
)
from ._typedef import (
    RealFunction, RealNFunction
)


class DifferenceQuotient:
    r"""
    Computes difference quotients for a one-dimensional real-valued function ``f``,
    :math:`f: \mathbb{R} \mapsto \mathbb{R}`, using step size ``h``.
    """
    def __init__(self, f: RealFunction, h: float):
        self._f  = f
        self._h = h

        self._forward = Forward(self.f, self.h)
        self._backward = Backward(self.f, self.h)
        self._central = Central(self.f, self.h)

    @property
    def f(self) -> RealFunction:
        r"""
        A one-dimension real-valued function, :math:`f: \mathbb{R} \mapsto \mathbb{R}`.
        """
        return self._f
    
    @property
    def h(self) -> float:
        """
        The step size used to compute difference quotients.
        """
        return self._h
    
    @h.setter
    def h(self, value: float) -> None:
        self._h = float(value)
        self.forward.h = self.backward.h = self.central.h = self.h

    @property
    def forward(self) -> Forward:
        """
        """
        return self._forward
    
    @property
    def backward(self) -> Backward:
        """
        """
        return self._backward
    
    @property
    def central(self) -> Central:
        """
        """
        return self._central

    def first(self, x: float) -> float:
        """
        Computes the first-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.first(x)
        except ValueError:
            try:
                fdiff = self.forward.first(x)
            except ValueError:
                fdiff = self.backward.first(x)

        return fdiff / self.h
    
    def second(self, x: float) -> float:
        """
        Computes the second-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.second(x)
        except ValueError:
            try:
                fdiff = self.forward.second(x)
            except ValueError:
                fdiff = self.backward.second(x)

        return fdiff / pow(self.h, 2)
    
    def nth(self, x: float, n: int) -> float:
        r"""
        Computes the ``n``\th-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.nth(x, n)
        except ValueError:
            try:
                fdiff = self.forward.nth(x, n)
            except ValueError:
                fdiff = self.backward.nth(x, n)

        return fdiff / pow(self.h, n)


class PDifferenceQuotient:
    r"""
    Computes difference quotients for a :math:`n`-dimensional real-valued function ``f``,
    :math:`f: {\mathbb{R}}^{n} \mapsto \mathbb{R}`, of ``dim`` dimensions using step size ``h``.
    """
    def __init__(self, f: RealNFunction, dim: int, h: float):
        self._f  = f
        self._dim = dim
        self._h = h

        self._forward = PForward(self.f, self.dim, self.h)
        self._backward = PForward(self.f, self.dim, self.h)
        self._central = PCentral(self.f, self.dim, self.h)

    @property
    def f(self) -> RealFunction:
        r"""
        A :math:`n`-dimension real-valued function, :math:`f: {\mathbb{R}}^{n} \mapsto \mathbb{R}`,
        of :py:attr:`dim` dimensions.
        """
        return self._f
    
    @property
    def dim(self) -> int:
        """
        The number of dimensions of the domain of :py:attr:`f`.
        """
        return self._dim
    
    @property
    def h(self) -> float:
        """
        The step size used to compute finite differences.
        """
        return self._h
    
    @h.setter
    def h(self, value: float) -> None:
        self._h = float(value)
        self.forward.h = self.backward.h = self.central.h = self.h

    @property
    def forward(self) -> PForward:
        """
        """
        return self._forward
    
    @property
    def backward(self) -> PBackward:
        """
        """
        return self._backward
    
    @property
    def central(self) -> PCentral:
        """
        """
        return self._central

    def first(self, x: np.ndarray) -> np.ndarray:
        """
        Computes the first-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.first(x)
        except ValueError:
            try:
                fdiff = self.forward.first(x)
            except ValueError:
                fdiff = self.backward.first(x)

        return fdiff / self.h
    
    def second(self, x: np.ndarray) -> np.ndarray:
        """
        Computes the second-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.second(x)
        except ValueError:
            try:
                fdiff = self.forward.second(x)
            except ValueError:
                fdiff = self.backward.second(x)

        return fdiff / pow(self.h, 2)
    
    def nth(self, x: np.ndarray, n: int) -> np.ndarray:
        r"""
        Computes the ``n``\th-order difference quotient for :py:attr:`f` at ``x`` using step size
        :py:attr:`h`.
        """
        try:
            fdiff = self.central.nth(x, n)
        except ValueError:
            try:
                fdiff = self.forward.nth(x, n)
            except ValueError:
                fdiff = self.backward.nth(x, n)

        return fdiff / pow(self.h, n)
