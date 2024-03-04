from dataclasses import dataclass, field
from functools import partial
from typing import Callable, Protocol

import numpy as np
from dyce import H
from dyce.evaluation import expandable, HResult
from numpy.typing import ArrayLike

from .core import BaseDice, Scalar

ExplodeDice = Callable[[BaseDice], BaseDice]


@dataclass(slots=True)
class BaseExplode(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice
    explode_depth: int = field(default=1)

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool: ...

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike: ...

    def histogram(self) -> H:
        @expandable
        def explode(compare: HResult, dice: HResult):
            return (
                dice.h + dice.outcome
                if self._compare_histogram_outcome(dice.outcome, compare.outcome)  # type: ignore
                else dice.outcome
            )

        return explode(self.compare.histogram(), self.dice.histogram())

    def max(self) -> int:
        return self.dice.max() * self.explode_depth

    def min(self) -> int:
        return self.dice.min()

    def generate(self, items: int) -> ArrayLike:
        results = np.zeros(items, dtype=np.int_)
        current_rolls = self.dice.generate(items)

        for _ in range(self.explode_depth + 1):
            results += current_rolls  # type: ignore
            compare_rolls = self.compare.generate(items)
            explode_mask = self._calculate_explode_mask(current_rolls, compare_rolls)

            if not np.any(explode_mask):
                break  # Exit if no dice explode in this iteration

            # Calculate how many dice need to be rerolled based on the explode_mask
            current_rolls = np.zeros(items, dtype=np.int_)
            current_rolls[explode_mask] = self.dice.generate(np.sum(explode_mask))  # type: ignore

        return results


@dataclass(slots=True)
class ExplodeEq(BaseExplode):
    def __str__(self) -> str:
        return f"{self.dice}x{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice == compare

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values == cmp_values


@dataclass(slots=True)
class ExplodeIfGreater(BaseExplode):

    def __str__(self) -> str:
        return f"{self.dice}x>{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice > compare

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values > cmp_values  # type: ignore


@dataclass(slots=True)
class ExplodeIfGreaterOrEq(BaseExplode):
    def __str__(self) -> str:
        return f"{self.dice}x>={self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice >= compare

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values >= cmp_values  # type: ignore


@dataclass(slots=True)
class ExplodeIfLess(BaseExplode):
    def __str__(self) -> str:
        return f"{self.dice}x<{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice < compare

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values < cmp_values  # type: ignore


@dataclass(slots=True)
class ExplodeIfLessOrEq(BaseExplode):
    def __str__(self) -> str:
        return f"{self.dice}x<={self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice <= compare

    @staticmethod
    def _calculate_explode_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values <= cmp_values  # type: ignore


def _wrap_scalar(value: BaseDice | int) -> BaseDice:
    if isinstance(value, int):
        value = Scalar(value)
    if not isinstance(value, BaseDice):
        raise TypeError("Explode only support other dices or integers")
    return value


class Explode:
    def __init__(self, explode_depth: int = 1) -> None:
        self.explode_depth = explode_depth

    def __eq__(self, value: BaseDice | int) -> ExplodeDice:  # type: ignore
        return partial(ExplodeEq, compare=_wrap_scalar(value), explode_depth=self.explode_depth)

    def __gt__(self, value: BaseDice | int) -> ExplodeDice:
        return partial(ExplodeIfGreater, compare=_wrap_scalar(value), explode_depth=self.explode_depth)

    def __ge__(self, value: BaseDice | int) -> ExplodeDice:
        return partial(ExplodeIfGreaterOrEq, compare=_wrap_scalar(value), explode_depth=self.explode_depth)

    def __lt__(self, value: BaseDice | int) -> ExplodeDice:
        return partial(ExplodeIfLess, compare=_wrap_scalar(value), explode_depth=self.explode_depth)

    def __le__(self, value: BaseDice | int) -> ExplodeDice:
        return partial(ExplodeIfLessOrEq, compare=_wrap_scalar(value), explode_depth=self.explode_depth)


class _ExplodeFactory:
    def __init__(self, dice: BaseDice, explode_depth: int = 1) -> None:
        self.dice = dice
        self.explode_depth = explode_depth

    def __eq__(self, value: BaseDice | int) -> ExplodeDice:  # type: ignore
        return ExplodeEq(self.dice, compare=_wrap_scalar(value), explode_depth=self.explode_depth)  # type: ignore

    def __gt__(self, value: BaseDice | int) -> ExplodeDice:
        return ExplodeIfGreater(self.dice, compare=_wrap_scalar(value), explode_depth=self.explode_depth)  # type: ignore

    def __ge__(self, value: BaseDice | int) -> ExplodeDice:
        return ExplodeIfGreaterOrEq(self.dice, compare=_wrap_scalar(value), explode_depth=self.explode_depth)  # type: ignore

    def __lt__(self, value: BaseDice | int) -> ExplodeDice:
        return ExplodeIfLess(self.dice, compare=_wrap_scalar(value), explode_depth=self.explode_depth)  # type: ignore

    def __le__(self, value: BaseDice | int) -> ExplodeDice:
        return ExplodeIfLessOrEq(self.dice, compare=_wrap_scalar(value), explode_depth=self.explode_depth)  # type: ignore
