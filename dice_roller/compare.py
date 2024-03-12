from dataclasses import dataclass
from functools import partial
from typing import Protocol

import numpy as np
from dyce import H
from dyce.evaluation import HResult, expandable
from numpy.typing import ArrayLike

from .core import BaseDice
from .misc import DiceModifier, _wrap_scalar


@dataclass(slots=True)
class BaseCompare(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]: ...

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool: ...

    @staticmethod
    def _modify_input_histogram(dice: H, compare: H) -> tuple[H, H]:
        return dice, compare

    def histogram(self) -> H:
        @expandable
        def cmp(dice: HResult, compare: HResult):
            if not self._compare_histogram_outcome(dice.outcome, compare.outcome):  # type: ignore
                return compare.outcome
            return dice.outcome

        return cmp(*self._modify_input_histogram(self.dice.histogram(), self.compare.histogram()))

    def generate(self, items: int) -> ArrayLike:
        result_rolls = self.dice.generate(items)
        cmp_rolls = self.compare.generate(items)
        return self._with_cap(result_rolls, cmp_rolls)  # type: ignore


@dataclass(slots=True)
class Lt(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}<{self.compare}"

    def max(self) -> int:
        return min(self.compare.max() - 1, self.dice.max())

    def min(self) -> int:
        return min(self.dice.min(), self.max())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice < compare

    @staticmethod
    def _modify_input_histogram(dice: H, compare: H) -> tuple[H, H]:
        return dice, compare - 1  # type: ignore

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.minimum(roll_values, (cmp_values - 1))  # type: ignore


@dataclass(slots=True)
class Le(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}<={self.compare}"

    def max(self) -> int:
        return min(self.compare.max(), self.dice.max())

    def min(self) -> int:
        return min(self.dice.min(), self.max())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice <= compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.minimum(roll_values, cmp_values)  # type: ignore


@dataclass(slots=True)
class Gt(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}>{self.compare}"

    def max(self) -> int:
        return max(self.dice.max(), self.compare.max() + 1)

    def min(self) -> int:
        return max(self.dice.min(), self.compare.min() + 1)

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice > compare

    @staticmethod
    def _modify_input_histogram(dice: H, compare: H) -> tuple[H, H]:
        return dice, compare + 1  # type: ignore

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.maximum(roll_values, (cmp_values + 1))  # type: ignore


@dataclass(slots=True)
class Ge(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}>={self.compare}"

    def max(self) -> int:
        return max(self.dice.max(), self.compare.max())

    def min(self) -> int:
        return max(self.dice.min(), self.compare.min())

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice >= compare

    @staticmethod
    def _with_cap(roll_values: ArrayLike, cmp_values: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        return np.maximum(roll_values, cmp_values)  # type: ignore


class Limit:
    def __gt__(self, value: BaseDice | int) -> DiceModifier:
        return partial(Gt, compare=_wrap_scalar(value))

    def __ge__(self, value: BaseDice | int) -> DiceModifier:
        return partial(Ge, compare=_wrap_scalar(value))

    def __lt__(self, value: BaseDice | int) -> DiceModifier:
        return partial(Lt, compare=_wrap_scalar(value))

    def __le__(self, value: BaseDice | int) -> DiceModifier:
        return partial(Le, compare=_wrap_scalar(value))
