from dataclasses import dataclass
from typing import Callable, Protocol

import numpy as np
from numpy.typing import ArrayLike
from dyce import H
from dyce.evaluation import expandable, HResult


from .core import BaseDice

ExplodeDice = Callable[[BaseDice], BaseDice]


@dataclass
class BaseCompare(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]: ...

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool: ...

    def histogram(self) -> H:
        @expandable
        def cmp(dice: HResult, compare: HResult):
            if self._compare_histogram_outcome(dice.outcome, compare.outcome):  # type: ignore
                return compare.outcome
            return dice.outcome

        return cmp(self.dice.histogram(), self.compare.histogram())

    def generate(self, items: int) -> ArrayLike:
        result_rolls = self.dice.generate(items)
        cmp_rolls = self.compare.generate(items)
        return self._with_cap(result_rolls, cmp_rolls)  # type: ignore


@dataclass
class Lt(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}<{self.compare}"

    def max(self) -> int:
        return min(self.compare.max() - 1, self.dice.max())

    def min(self) -> int:
        return min(self.dice.min(), self.max())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice > compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.minimum(roll_values, (cmp_values - 1))  # type: ignore


@dataclass
class Le(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}<={self.compare}"

    def max(self) -> int:
        return min(self.compare.max(), self.dice.max())

    def min(self) -> int:
        return min(self.dice.min(), self.max())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice >= compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.minimum(roll_values, cmp_values)  # type: ignore


@dataclass
class Gt(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}>{self.compare}"

    def max(self) -> int:
        return max(self.dice.max(), self.compare.max() + 1)

    def min(self) -> int:
        return max(self.dice.min(), self.compare.min() + 1)

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice < compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.maximum(roll_values, (cmp_values + 1))  # type: ignore


@dataclass
class Ge(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}>={self.compare}"

    def max(self) -> int:
        return max(self.dice.max(), self.compare.max())

    def min(self) -> int:
        return max(self.dice.min(), self.compare.min())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice <= compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.maximum(roll_values, cmp_values)  # type: ignore
