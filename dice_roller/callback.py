from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from numpy.typing import ArrayLike

from .core import BaseDice


@dataclass(slots=True)
class WithRollCallback(BaseDice):
    dice: BaseDice
    roll_callback: Callable[[int], None]

    def __str__(self) -> str:
        return self.dice.__str__()

    def max(self) -> int:
        return self.dice.max()

    def min(self) -> int:
        return self.dice.min()

    def roll(self) -> int:
        result = self.dice.roll()
        if self.roll_callback is not None:
            self.roll_callback(result)
        return result

    def generate(self, items: int) -> ArrayLike:
        return self.dice.generate(items)


@dataclass(slots=True)
class WithGenerateCallback(BaseDice):
    dice: BaseDice
    generate_callback: Callable[[ArrayLike], None]

    def __str__(self) -> str:
        return self.dice.__str__()

    def max(self) -> int:
        return self.dice.max()

    def min(self) -> int:
        return self.dice.min()

    def generate(self, items: int) -> ArrayLike:
        result = self.dice.generate(items)
        if self.generate_callback is not None:
            self.generate_callback(result)
        return result
