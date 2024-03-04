from dataclasses import dataclass, field

import numpy as np
from dyce import H
from numpy.typing import ArrayLike

from .core import BaseDice


@dataclass(slots=True)
class DiceAdd(BaseDice):
    items: tuple[BaseDice, ...]

    def histogram(self) -> H:
        return sum(i.histogram() for i in self.items)  # type: ignore

    def __str__(self) -> str:
        return "(" + " + ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        return np.sum([i.max() for i in self.items])

    def min(self) -> int:
        return np.sum([i.min() for i in self.items])

    def generate(self, items: int) -> ArrayLike:
        res = np.zeros(items, dtype=np.int_)
        for i in self.items:
            res += i.generate(items)  # type: ignore
        return res


@dataclass(slots=True)
class DiceSub(BaseDice):
    items: tuple[BaseDice, ...]

    def histogram(self) -> H:
        result = self.items[0].histogram()
        for i in self.items[1:]:
            result -= i.histogram()  # type: ignore
        return result  # type: ignore

    def __str__(self) -> str:
        return "(" + " - ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        # The maximum value for subtraction is calculated by subtracting the min values of all but the first dice from the max value of the first dice.
        max_first_item = self.items[0].max()
        sum_of_max_of_others = np.sum([i.min() for i in self.items[1:]])
        return max_first_item - sum_of_max_of_others

    def min(self) -> int:
        # The minimum value for subtraction is calculated by subtracting the max values of all but the first dice from the min value of the first dice.
        min_first_item = self.items[0].min()
        sum_of_max_of_others = np.sum([i.max() for i in self.items[1:]])
        min_value = min_first_item - sum_of_max_of_others
        return min_value

    def generate(self, items: int) -> ArrayLike:
        result = self.items[0].generate(items)
        for item in self.items[1:]:
            result -= item.generate(items)  # type: ignore
        return result


@dataclass(slots=True)
class DiceMul(BaseDice):
    items: tuple[BaseDice, ...]

    def histogram(self) -> H:
        result = self.items[0].histogram()
        for i in self.items[1:]:
            result *= i.histogram()  # type: ignore
        return result  # type: ignore

    def __str__(self) -> str:
        return "(" + " * ".join(str(i) for i in self.items) + ")"

    def max(self) -> int:
        # Calculate the maximum possible outcome by multiplying the maximum values of all included dice.
        return int(np.prod([i.max() for i in self.items]))

    def min(self) -> int:
        # Calculate the minimum possible outcome by multiplying the minimum values of all included dice.
        return int(np.prod([i.min() for i in self.items]))

    def generate(self, items: int) -> ArrayLike:
        res = np.ones(items, dtype=np.int_)
        for i in self.items:
            res *= i.generate(items)  # type: ignore
        return res


@dataclass(slots=True)
class DiceDiv(BaseDice):
    items: tuple[BaseDice, ...]

    def histogram(self) -> H:
        result = self.items[0].histogram()
        for i in self.items[1:]:
            result /= i.histogram()  # type: ignore
        return result  # type: ignore

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
        result = self.items[0].generate(items)
        for item in self.items[1:]:
            result //= item.generate(items)  # type: ignore
        return result
