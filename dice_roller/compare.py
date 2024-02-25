from dataclasses import dataclass
from typing import Callable, Protocol

from numpy.typing import ArrayLike

from .core import BaseDice

ExplodeDice = Callable[[BaseDice], BaseDice]


@dataclass
class BaseCompare(BaseDice, Protocol):
    dice: BaseDice
    compare: BaseDice

    def _calculate_compare_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike: ...

    def generate(self, items: int) -> ArrayLike:
        result_rolls = self.dice.generate(items)
        cmp_rolls = self.compare.generate(items)

        # Instead of a fixed comparison to min_value, we compare each roll to its corresponding dynamic minimum
        cmp_mask = self._calculate_compare_mask(result_rolls, cmp_rolls)
        result_rolls[cmp_mask] = cmp_rolls[cmp_mask]  # type: ignore

        return result_rolls


@dataclass
class Min(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}min{self.compare}"

    def max(self) -> int:
        return self.dice.max()

    def min(self) -> int:
        # The effective minimum is the specified min_value or the dice's minimum, whichever is higher
        return max(self.compare.min(), self.dice.min())

    def _calculate_compare_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values < cmp_values  # type: ignore


@dataclass
class Max(BaseCompare):
    def __str__(self) -> str:
        return f"{self.dice}max{self.compare}"

    def max(self) -> int:
        # The effective maximum is the specified max_value or the dice's maximum, whichever is lower
        return min(self.compare.max(), self.dice.max())

    def min(self) -> int:
        return self.dice.min()

    def _calculate_compare_mask(self, roll_values: ArrayLike, cmp_values: ArrayLike) -> ArrayLike:
        return roll_values > cmp_values  # type: ignore
