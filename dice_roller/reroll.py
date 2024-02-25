from dataclasses import dataclass, field
from functools import partial
from typing import Callable, Protocol

import numpy as np
from numpy.typing import ArrayLike

from .core import BaseDice, Scalar

RerollDice = Callable[[BaseDice], BaseDice]


@dataclass
class BaseReroll(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice
    reroll_limit: int = field(default=1)

    def max(self) -> int:
        return self.dice.max()

    def min(self) -> int:
        return self.dice.min()

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike: ...

    def generate(self, items: int) -> ArrayLike:
        result = self.dice.generate(items)
        reroll_count = 0

        # Generate the comparison values once per reroll cycle
        compare_values = self.compare.generate(items)

        reroll_mask = self._calculate_reroll_mask(result, compare_values)
        while np.any(reroll_mask) and reroll_count < self.reroll_limit:
            rerolls = self.dice.generate(np.sum(reroll_mask))
            result[reroll_mask] = rerolls  # type: ignore
            reroll_count += 1
            # Re-evaluate reroll conditions if necessary
            if reroll_count < self.reroll_limit:
                compare_values = self.compare.generate(items)
                reroll_mask = self._calculate_reroll_mask(result, compare_values)

        return result


@dataclass
class RerollEq(BaseReroll):

    def __str__(self) -> str:
        return f"{self.dice}r{self.compare}"

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values == cmp_values


@dataclass
class RerollIfGreater(BaseReroll):

    def __str__(self) -> str:
        return f"{self.dice}r>{self.compare}"

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values > cmp_values  # type: ignore


@dataclass
class RerollIfGreaterOrEq(BaseReroll):

    def __str__(self) -> str:
        return f"{self.dice}r>={self.compare}"

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values >= cmp_values  # type: ignore


@dataclass
class RerollIfLess(BaseReroll):

    def __str__(self) -> str:
        return f"{self.dice}r<{self.compare}"

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values < cmp_values  # type: ignore


@dataclass
class RerollIfLessOrEq(BaseReroll):

    def __str__(self) -> str:
        return f"{self.dice}r<={self.compare}"

    def _calculate_reroll_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values <= cmp_values  # type: ignore


def _wrap_scalar(value: BaseDice | int) -> BaseDice:
    if isinstance(value, int):
        value = Scalar(value)
    if not isinstance(value, BaseDice):
        raise TypeError("Reroll only support other dices or integers")
    return value


class Reroll:
    def __init__(self, reroll_limit: int = 1) -> None:
        self.reroll_limit = reroll_limit

    def __eq__(self, value: BaseDice | int) -> RerollDice:  # type: ignore
        return partial(RerollEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __gt__(self, value: BaseDice | int) -> RerollDice:
        return partial(RerollIfGreater, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __ge__(self, value: BaseDice | int) -> RerollDice:
        return partial(RerollIfGreaterOrEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __lt__(self, value: BaseDice | int) -> RerollDice:
        return partial(RerollIfLess, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __le__(self, value: BaseDice | int) -> RerollDice:
        return partial(RerollIfLessOrEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)