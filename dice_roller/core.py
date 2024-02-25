from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import numpy as np
from numpy.typing import ArrayLike

from .random import Rng


@runtime_checkable
class BaseDice(Protocol):
    STATISTIC_SIMULATION_SAMPLES: int = 1_000_000

    def generate(self, items: int) -> ArrayLike: ...

    def max(self) -> int: ...

    def min(self) -> int: ...

    def __str__(self) -> str:
        return super().__str__()

    def average(self, samples: int | None = None) -> float:
        if samples is None:
            samples = self.STATISTIC_SIMULATION_SAMPLES
        return np.average(self.generate(samples))  # type: ignore

    def median(self, samples: int | None = None) -> float:
        if samples is None:
            samples = self.STATISTIC_SIMULATION_SAMPLES
        return np.median(self.generate(samples))  # type: ignore

    def mean(self, samples: int | None = None) -> float:
        if samples is None:
            samples = self.STATISTIC_SIMULATION_SAMPLES
        return np.mean(self.generate(samples))  # type: ignore

    def std(self, samples: int | None = None) -> float:
        if samples is None:
            samples = self.STATISTIC_SIMULATION_SAMPLES
        return np.std(self.generate(samples))  # type: ignore

    def roll(self) -> int:
        return np.sum(self.generate(1))

    def __pow__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")

        return DiceMany(total=self, dice=other)

    def __rpow__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")

        return DiceMany(total=other, dice=self)

    def __add__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")

        if isinstance(other, DiceAdd):
            items = other.items
        else:
            items = [other]

        if isinstance(self, DiceAdd):
            return DiceAdd([*self.items, *items])

        return DiceAdd([self, *items])

    def __radd__(self, other):
        if isinstance(other, int):
            return DiceAdd([Scalar(other), self])

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only sub other dices or integers")

        if isinstance(other, DiceSub):
            items = other.items
        else:
            items = [other]

        if isinstance(self, DiceSub):
            return DiceSub([*self.items, *items])
        return DiceSub([self, *items])

    def __rsub__(self, other):
        if isinstance(other, int):
            return DiceSub([Scalar(other), self])

        if not isinstance(other, BaseDice):
            raise TypeError("Can only sub other dices or integers")
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only mul other dices or integers")

        if isinstance(other, DiceMul):
            items = other.items
        else:
            items = [other]

        if isinstance(self, DiceMul):
            return DiceMul([*self.items, *items])
        return DiceMul([self, *items])

    def __rmul__(self, other):
        if isinstance(other, int):
            return DiceMul([Scalar(other), self])
        if not isinstance(other, BaseDice):
            raise TypeError("Can only mul other dices or integers")
        return self

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        if isinstance(other, DiceDiv):
            items = other.items
        else:
            items = [other]

        if isinstance(self, DiceDiv):
            return DiceDiv([*self.items, *items])
        return DiceDiv([self, *items])

    def __rtruediv__(self, other):
        if isinstance(other, int):
            return DiceDiv([Scalar(other), self])
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")
        return self

    __floordiv__ = __truediv__  # type: ignore
    __rfloordiv__ = __rtruediv__  # type: ignore

    def __ge__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Min

        return Min(dice=self, compare=other)  # type: ignore

    def __le__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Max

        return Max(dice=self, compare=other)  # type: ignore


@dataclass
class Scalar(BaseDice):
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def max(self) -> int:
        return self.value

    def min(self) -> int:
        return self.value

    def generate(self, items: int) -> ArrayLike:
        return np.full(items, self.value)


@dataclass
class Dice(BaseDice):
    sides: int
    minimal: int = field(default=1)

    def __str__(self) -> str:
        if self.minimal == 1:
            return f"d{self.sides}"
        return f"d[{self.minimal} to {self.sides}]"

    def max(self) -> int:
        return self.sides

    def min(self) -> int:
        return self.minimal

    def generate(self, items: int) -> ArrayLike:
        return Rng().rng.integers(low=self.minimal, high=self.sides + 1, size=items)


@dataclass
class RangeDice(BaseDice):
    min_value: int
    max_value: int

    def __str__(self) -> str:
        return f"d[{self.min_value} to {self.max_value}]"

    def max(self) -> int:
        return self.max_value - 1

    def min(self) -> int:
        return self.min_value

    def generate(self, items: int) -> ArrayLike:
        return Rng().rng.integers(low=self.min_value, high=self.max_value, size=items)


@dataclass
class DiceAdd(BaseDice):
    items: list[BaseDice]

    def __str__(self) -> str:
        return "(" + " + ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        return np.sum([i.max() for i in self.items])

    def min(self) -> int:
        return np.sum([i.min() for i in self.items])

    def generate(self, items: int) -> ArrayLike:
        if not self.items:
            return np.zeros(items, dtype=np.int_)

        res = np.zeros(items, dtype=np.int_)
        for i in self.items:
            res += i.generate(items)  # type: ignore
        return res


@dataclass
class DiceMany(BaseDice):
    total: BaseDice
    dice: BaseDice

    def __str__(self) -> str:
        return f"{self.total}{self.dice}"

    def max(self) -> int:
        return self.dice.max() * self.total.max()

    def min(self) -> int:
        return self.dice.min() * self.total.min()

    def generate(self, items: int) -> np.ndarray:
        total_rolls = self.total.generate(items)
        max_rolls = np.max(total_rolls)

        result = np.zeros(items, dtype=np.int_)

        for roll_count in range(1, max_rolls + 1):
            mask = total_rolls >= roll_count  # type: ignore
            num_items_this_round = np.sum(mask)

            # If no items require processing, exit the loop early
            if num_items_this_round == 0:
                break

            # Generate and sum the dice rolls for items requiring them
            this_round_rolls = self.dice.generate(num_items_this_round)
            result[mask] += this_round_rolls  # type: ignore

        return result


@dataclass
class DiceSub(BaseDice):
    items: list[BaseDice]
    min_value: None | int = field(default=None)

    def __str__(self) -> str:
        return "(" + " - ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        # The maximum value for subtraction is calculated by subtracting the min values of all but the first dice from the max value of the first dice.
        if not self.items:
            return 0  # or raise an error

        max_first_item = self.items[0].max()
        sum_of_max_of_others = np.sum([i.min() for i in self.items[1:]])
        return max_first_item - sum_of_max_of_others

    def min(self) -> int:
        # The minimum value for subtraction is calculated by subtracting the max values of all but the first dice from the min value of the first dice.
        if not self.items:
            return 0  # or raise an error

        min_first_item = self.items[0].min()
        sum_of_max_of_others = np.sum([i.max() for i in self.items[1:]])
        min_value = min_first_item - sum_of_max_of_others
        if self.min_value and min_value < self.min_value:
            return self.min_value
        return min_value

    def generate(self, items: int) -> ArrayLike:
        if not self.items:
            return np.zeros(items, dtype=np.int_)

        result = self.items[0].generate(items)
        for item in self.items[1:]:
            result -= item.generate(items)  # type: ignore
            if self.min_value is not None:
                result = np.maximum(self.min_value, result)  # Ensure all values are > 0
        return result


@dataclass
class DiceMul(BaseDice):
    items: list[BaseDice]

    def __str__(self) -> str:
        return "(" + " * ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        # Calculate the maximum possible outcome by multiplying the maximum values of all included dice.
        return int(np.prod([i.max() for i in self.items]))

    def min(self) -> int:
        # Calculate the minimum possible outcome by multiplying the minimum values of all included dice.
        return int(np.prod([i.min() for i in self.items]))

    def generate(self, items: int) -> ArrayLike:
        if not self.items:
            return np.zeros(items, dtype=np.int_)

        res = np.ones(items, dtype=np.int_)
        for i in self.items:
            res *= i.generate(items)  # type: ignore
        return res


@dataclass
class DiceDiv(BaseDice):
    items: list[BaseDice]

    def __str__(self) -> str:
        return "(" + " / ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        # Divide the max value of the first item by the product of min values of the rest.
        numerator = self.items[0].max()
        # Calculate the product of min values for the rest of the items.
        denominators_product = np.prod([i.min() for i in self.items[1:]])
        # Perform division, ensuring no division by zero.
        return int(numerator // denominators_product if denominators_product else 0)

    def min(self) -> int:
        # Divide the min value of the first item by the product of max values of the rest.
        numerator = self.items[0].min()
        # Calculate the product of max values for the rest of the items.
        denominators_product = np.prod([i.max() for i in self.items[1:]])
        # Perform division, ensuring no division by zero.
        return int(numerator // denominators_product if denominators_product else 0)

    def generate(self, items: int) -> ArrayLike:
        if not self.items:
            return np.zeros(items, dtype=np.int_)

        result = self.items[0].generate(items)
        for item in self.items[1:]:
            result //= item.generate(items)  # type: ignore
        return result
