from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from dyce import H, P
from dyce.evaluation import HResult, expandable
from numpy.typing import ArrayLike

from .core import BaseDice, DiceMany, Scalar


@dataclass(slots=True)
class KeepHighest(BaseDice):
    dice: BaseDice
    keep: BaseDice = field(default_factory=lambda: Scalar(1))
    of: BaseDice = field(default_factory=lambda: Scalar(1))

    def __post_init__(self):
        if isinstance(self.dice, DiceMany):
            self.of = self.dice.total
            self.dice = self.dice.dice
        if isinstance(self.keep, int):
            self.keep = Scalar(self.keep)

    def histogram(self) -> H:
        @expandable
        def kh(dice: HResult, keep: HResult, of: HResult):
            return (of.outcome @ P(dice.h)).h(slice(-keep.outcome, None))  # type: ignore

        return kh(self.dice.histogram(), self.keep.histogram(), self.of.histogram())

    def __str__(self) -> str:
        keep = str(self.keep)
        if isinstance(self.keep, Scalar) and self.keep.value == 1:
            keep = ""
        return f"{self.of}{self.dice}kh{keep}"

    def max(self) -> int:
        # Assuming the best rolls are kept, the maximum is the highest dice value times the maximum number of keeps,
        # but it cannot exceed the total number of dice rolled.
        return self.dice.max() * min(self.keep.max(), self.of.max())

    def min(self) -> int:
        # If keeping less than or equal to the number of dice rolled, the minimum would still be the dice's minimum value
        # times the minimum number of keeps, as we're assuming the least favorable (lowest) high rolls are kept.
        return self.dice.min() * self.keep.min()

    def generate(self, items: int) -> ArrayLike:
        of_rolls = self.of.generate(items)
        dice_rolls = self.dice.generate(np.sum(of_rolls))
        keep_rolls = self.keep.generate(items)
        results = np.empty(items, dtype=np.int_)

        start_idx = 0
        for i in range(items):
            num_rolls = of_rolls[i]  # type: ignore
            keep = min(keep_rolls[i], num_rolls)  # type: ignore
            results[i] = np.sum(np.sort(dice_rolls[start_idx : start_idx + num_rolls])[-keep:])  # type: ignore
            start_idx += num_rolls  # type: ignore

        return results


@dataclass(slots=True)
class KeepLowest(BaseDice):
    dice: BaseDice
    keep: BaseDice = field(default_factory=lambda: Scalar(1))
    of: BaseDice = field(default_factory=lambda: Scalar(1))

    def __post_init__(self):
        if isinstance(self.dice, DiceMany):
            self.of = self.dice.total
            self.dice = self.dice.dice
        if isinstance(self.keep, int):
            self.keep = Scalar(self.keep)

    def histogram(self) -> H:
        @expandable
        def kl(dice: HResult, keep: HResult, of: HResult):
            return (of.outcome @ P(dice.h)).h(slice(None, keep.outcome))  # type: ignore

        return kl(self.dice.histogram(), self.keep.histogram(), self.of.histogram())

    def __str__(self) -> str:
        keep = str(self.keep)
        if isinstance(self.keep, Scalar) and self.keep.value == 1:
            keep = ""
        return f"{self.of}{self.dice}kl{keep}"

    def max(self) -> int:
        # For keeping the lowest, the max is now the dice's max value times the minimum number of keeps,
        # because even when keeping the lowest, the max scenario would involve the highest possible "low" values.
        return self.dice.max() * min(self.keep.max(), self.of.max())

    def min(self) -> int:
        # The minimum is the dice's minimum value times the number of keeps, assuming the lowest possible outcomes are kept.
        return self.dice.min() * self.keep.min()

    def generate(self, items: int) -> ArrayLike:
        of_rolls = self.of.generate(items)
        dice_rolls = self.dice.generate(np.sum(of_rolls))
        keep_rolls = self.keep.generate(items)
        results = np.empty(items, dtype=np.int_)

        start_idx = 0
        for i in range(items):
            num_rolls = of_rolls[i]  # type: ignore
            keep = min(keep_rolls[i], num_rolls)  # type: ignore
            results[i] = np.sum(np.sort(dice_rolls[start_idx : start_idx + num_rolls])[:keep])  # type: ignore
            start_idx += num_rolls  # type: ignore

        return results


@dataclass(slots=True)
class DropHighest(BaseDice):
    dice: BaseDice
    drop: BaseDice = field(default_factory=lambda: Scalar(1))
    of: BaseDice = field(default_factory=lambda: Scalar(1))

    def __post_init__(self):
        if isinstance(self.dice, DiceMany):
            self.of = self.dice.total
            self.dice = self.dice.dice
        if isinstance(self.drop, int):
            self.drop = Scalar(self.drop)

    def histogram(self) -> H:
        @expandable
        def dh(dice: HResult, drop: HResult, of: HResult):
            return (of.outcome @ P(dice.h)).h(slice(None, drop.outcome))  # type: ignore

        return dh(self.dice.histogram(), self.drop.histogram(), self.of.histogram())

    def __str__(self) -> str:
        drop = str(self.drop)
        if isinstance(self.drop, Scalar) and self.drop.value == 1:
            drop = ""
        return f"{self.of}{self.dice}dh{drop}"

    def max(self) -> int:
        # Maximum possible value after dropping the highest rolls
        return self.dice.max() * (self.of.max() - self.drop.min())

    def min(self) -> int:
        # Minimum possible value after dropping the highest rolls
        return self.dice.min() * max(0, self.of.min() - self.drop.max())

    def generate(self, items: int) -> np.ndarray:
        of_rolls = self.of.generate(items)
        drop_rolls = self.drop.generate(items)
        dice_rolls = self.dice.generate(np.sum(of_rolls))

        # Initialize results array
        results = np.empty(items, dtype=np.int_)

        start_idx = 0
        for i in range(items):
            num_rolls = of_rolls[i]  # type: ignore
            drop = min(num_rolls, drop_rolls[i])  # type: ignore

            sorted_rolls = np.sort(dice_rolls[start_idx : start_idx + num_rolls])  # type: ignore
            results[i] = np.sum(sorted_rolls[:-drop] if drop > 0 else sorted_rolls)  # type: ignore

            start_idx += num_rolls  # type: ignore

        return results


@dataclass(slots=True)
class DropLowest(BaseDice):
    dice: BaseDice
    drop: BaseDice = field(default_factory=lambda: Scalar(1))
    of: BaseDice = field(default_factory=lambda: Scalar(2))  # Adjusted default for consistency

    def __post_init__(self):
        if isinstance(self.dice, DiceMany):
            self.of = self.dice.total
            self.dice = self.dice.dice
        if isinstance(self.drop, int):
            self.drop = Scalar(self.drop)

    def histogram(self) -> H:
        @expandable
        def dh(dice: HResult, drop: HResult, of: HResult):
            return (of.outcome @ P(dice.h)).h(slice(-drop.outcome, None))  # type: ignore

        return dh(self.dice.histogram(), self.drop.histogram(), self.of.histogram())

    def __str__(self) -> str:
        drop = str(self.drop)
        if isinstance(self.drop, Scalar) and self.drop.value == 1:
            drop = ""
        return f"{self.of}{self.dice}dl{drop}"

    def max(self) -> int:
        # Maximum possible value after dropping the lowest rolls.
        # The max calculation now considers the possibility of dropping less valuable rolls.
        return self.dice.max() * (self.of.max() - self.drop.min())

    def min(self) -> int:
        # Minimum possible value after dropping the lowest rolls.
        # Adjusted to consider the effect of dropping the lowest possible rolls.
        return self.dice.min() * max(0, self.of.min() - self.drop.max())

    def generate(self, items: int) -> np.ndarray:
        of_rolls = self.of.generate(items)
        drop_rolls = self.drop.generate(items)
        dice_rolls = self.dice.generate(np.sum(of_rolls))

        results = np.empty(items, dtype=np.int_)

        start_idx = 0
        for i in range(items):
            num_rolls = of_rolls[i]  # type: ignore
            drop = min(num_rolls, drop_rolls[i])  # type: ignore

            sorted_rolls = np.sort(dice_rolls[start_idx : start_idx + num_rolls])  # type: ignore
            results[i] = np.sum(sorted_rolls[drop:] if drop > 0 else sorted_rolls)  # type: ignore

            start_idx += num_rolls  # type: ignore

        return results
