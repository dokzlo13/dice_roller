from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import ArrayLike

from .core import BaseDice


@dataclass
class KeepHighest(BaseDice):
    dice: BaseDice
    of: int = field(default=2)
    keep: int = field(default=1)

    def __post_init__(self):
        # Validate that `of` is greater than or equal to `keep`
        if self.of < self.keep:
            raise ValueError("`of` must be greater than or equal to `keep`")

    def __str__(self) -> str:
        str_repr = f"{self.dice}kh{self.keep}"
        if self.of != 2:
            str_repr += f"of{self.of}"
        return str_repr

    def max(self) -> int:
        return self.dice.max() * self.keep

    def min(self) -> int:
        return self.dice.min() * self.keep

    def generate(self, items: int) -> ArrayLike:
        # Initialize a result array
        result = np.zeros((self.of, items), dtype=np.int_)
        for i in range(self.of):
            result[i, :] = self.dice.generate(items)

        # Sort each column and sum the `keep` highest values
        sorted_result = np.sort(result, axis=0)
        top_keeps = sorted_result[-self.keep :, :]  # Get the `keep` highest rolls
        return np.sum(top_keeps, axis=0)  # Sum the `keep` highest values for each item


@dataclass
class KeepLowest(BaseDice):
    dice: BaseDice
    of: int = field(default=2)
    keep: int = field(default=1)

    def __post_init__(self):
        # Validate that `of` is greater than or equal to `keep`
        if self.of < self.keep:
            raise ValueError("`of` must be greater than or equal to `keep`")

    def __str__(self) -> str:
        str_repr = f"{self.dice}kl{self.keep}"
        if self.of != 2:
            str_repr += f"of{self.of}"
        return str_repr

    def max(self) -> int:
        # Return the sum of `keep` highest possible dice roll values
        # Since this is KeepLowest, we adapt the logic for max accordingly
        return self.dice.max() * self.keep

    def min(self) -> int:
        # Return the sum of `keep` lowest possible dice roll values
        return self.dice.min() * self.keep

    def generate(self, items: int) -> ArrayLike:
        # Initialize a result array
        result = np.zeros((self.of, items), dtype=np.int_)
        for i in range(self.of):
            result[i, :] = self.dice.generate(items)

        # Sort each column and sum the `keep` lowest values
        sorted_result = np.sort(result, axis=0)
        bottom_keeps = sorted_result[: self.keep, :]  # Get the `keep` lowest rolls
        return np.sum(bottom_keeps, axis=0)  # Sum the `keep` lowest values for each item


@dataclass
class DropHighest(BaseDice):
    dice: BaseDice
    of: int = field(default=2)
    drop: int = field(default=1)

    def __post_init__(self):
        if self.of < self.drop:
            raise ValueError("`of` must be greater than or equal to `drop`")

    def __str__(self) -> str:
        str_repr = f"{self.dice}dh{self.drop}"
        if self.of != 2:
            str_repr += f"of{self.of}"
        return str_repr

    def max(self) -> int:
        # Adapted to account for dropping the highest rolls
        return self.dice.max() * (self.of - self.drop)

    def min(self) -> int:
        # Adapted to account for dropping the highest rolls
        return self.dice.min() * (self.of - self.drop)

    def generate(self, items: int) -> ArrayLike:
        result = np.zeros((self.of, items), dtype=np.int_)
        for i in range(self.of):
            result[i, :] = self.dice.generate(items)

        sorted_result = np.sort(result, axis=0)
        # Drop the `keep` highest rolls and sum the rest
        if self.of > self.drop:
            dropped_keeps = sorted_result[: -self.drop, :]
        else:
            dropped_keeps = np.zeros((0, items), dtype=np.int_)  # If dropping all, result is zeros
        return np.sum(dropped_keeps, axis=0)


@dataclass
class DropLowest(BaseDice):
    dice: BaseDice
    of: int = field(default=2)
    drop: int = field(default=1)

    def __post_init__(self):
        if self.of < self.drop:
            raise ValueError("`of` must be greater than or equal to `drop`")

    def __str__(self) -> str:
        str_repr = f"{self.dice}dl{self.drop}"
        if self.of != 2:
            str_repr += f"of{self.of}"
        return str_repr

    def max(self) -> int:
        # Adapted to account for dropping the lowest rolls
        return self.dice.max() * (self.of - self.drop)

    def min(self) -> int:
        # Adapted to account for dropping the lowest rolls
        return self.dice.min() * (self.of - self.drop)

    def generate(self, items: int) -> ArrayLike:
        result = np.zeros((self.of, items), dtype=np.int_)
        for i in range(self.of):
            result[i, :] = self.dice.generate(items)

        sorted_result = np.sort(result, axis=0)
        # Drop the `keep` lowest rolls and sum the rest
        if self.of > self.drop:
            dropped_keeps = sorted_result[self.drop :, :]
        else:
            dropped_keeps = np.zeros((0, items), dtype=np.int_)  # If dropping all, result is zeros
        return np.sum(dropped_keeps, axis=0)
