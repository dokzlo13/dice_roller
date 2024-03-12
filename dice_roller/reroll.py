from dataclasses import dataclass, field
from functools import partial
from typing import Protocol

import numpy as np
from dyce import H
from dyce.evaluation import HResult, expandable
from numpy.typing import ArrayLike

from .core import BaseDice
from .misc import DiceModifier, _wrap_scalar


@dataclass(slots=True)
class BaseReroll(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice
    reroll_limit: int = field(default=1)

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool: ...

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike: ...

    def max(self) -> int:
        return self.dice.max()

    def min(self) -> int:
        return self.dice.min()

    def histogram(self) -> H:
        dice_hist = self.dice.histogram()

        @expandable(sentinel=dice_hist)
        def _reroll(compare: HResult, dice: HResult):
            if self._compare_histogram_outcome(dice.outcome, compare.outcome):  # type: ignore
                # Replace a roll with rerolled dice
                return _reroll(compare.h, dice.h)  # type: ignore
            else:
                return dice.outcome

        return _reroll(self.compare.histogram(), dice_hist, limit=self.reroll_limit - 1)  # type: ignore

    def generate(self, items: int) -> ArrayLike:
        result = self.dice.generate(items)
        for _ in range(self.reroll_limit):
            compare_values = self.compare.generate(items)
            reroll_mask = self._calculate_reroll_mask(result, compare_values)

            if not np.any(reroll_mask):
                break

            rerolls = self.dice.generate(np.sum(reroll_mask))
            result[reroll_mask] = rerolls  # type: ignore

        return result


@dataclass(slots=True)
class RerollEq(BaseReroll):
    def __str__(self) -> str:
        return f"{self.dice}r{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice == compare

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values == cmp_values


@dataclass(slots=True)
class RerollIfGreater(BaseReroll):
    def __str__(self) -> str:
        return f"{self.dice}r>{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice > compare

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values > cmp_values  # type: ignore


@dataclass(slots=True)
class RerollIfGreaterOrEq(BaseReroll):
    def __str__(self) -> str:
        return f"{self.dice}r>={self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice >= compare

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values >= cmp_values  # type: ignore


@dataclass(slots=True)
class RerollIfLess(BaseReroll):
    def __str__(self) -> str:
        return f"{self.dice}r<{self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice < compare

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values < cmp_values  # type: ignore


@dataclass(slots=True)
class RerollIfLessOrEq(BaseReroll):
    def __str__(self) -> str:
        return f"{self.dice}r<={self.compare}"

    @staticmethod
    def _compare_histogram_outcome(dice: int, compare: int) -> bool:
        return dice <= compare

    @staticmethod
    def _calculate_reroll_mask(roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values <= cmp_values  # type: ignore


class Reroll:
    def __init__(self, reroll_limit: int = 1) -> None:
        self.reroll_limit = reroll_limit

    def __eq__(self, value: BaseDice | int) -> DiceModifier:  # type: ignore
        return partial(RerollEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __gt__(self, value: BaseDice | int) -> DiceModifier:
        return partial(RerollIfGreater, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __ge__(self, value: BaseDice | int) -> DiceModifier:
        return partial(RerollIfGreaterOrEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __lt__(self, value: BaseDice | int) -> DiceModifier:
        return partial(RerollIfLess, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)

    def __le__(self, value: BaseDice | int) -> DiceModifier:
        return partial(RerollIfLessOrEq, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)


class _RerollFactory:
    def __init__(self, dice: BaseDice, reroll_limit: int = 1) -> None:
        self.dice = dice
        self.reroll_limit = reroll_limit

    def __eq__(self, value: BaseDice | int) -> BaseReroll:  # type: ignore
        return RerollEq(dice=self.dice, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)  # type: ignore

    def __gt__(self, value: BaseDice | int) -> BaseReroll:
        return RerollIfGreater(dice=self.dice, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)  # type: ignore

    def __ge__(self, value: BaseDice | int) -> BaseReroll:
        return RerollIfGreaterOrEq(dice=self.dice, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)  # type: ignore

    def __lt__(self, value: BaseDice | int) -> BaseReroll:
        return RerollIfLess(dice=self.dice, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)  # type: ignore

    def __le__(self, value: BaseDice | int) -> BaseReroll:
        return RerollIfLessOrEq(dice=self.dice, compare=_wrap_scalar(value), reroll_limit=self.reroll_limit)  # type: ignore
