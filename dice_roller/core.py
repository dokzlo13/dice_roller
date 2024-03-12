from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import Protocol, runtime_checkable

import numpy as np
from dyce import H
from dyce.evaluation import expandable
from numpy.typing import ArrayLike

from .random import Rng


@runtime_checkable
class BaseDice(Protocol):

    # Interface methods

    def generate(self, items: int) -> ArrayLike: ...

    def max(self) -> int: ...

    def min(self) -> int: ...

    def __str__(self) -> str:
        return super().__str__()

    def histogram(self) -> H: ...

    # Base roll

    def roll(self) -> int:
        return np.sum(self.generate(1))

    # Modifiers

    def kh(self, keep: BaseDice | int = 1) -> BaseDice:
        from .transformations import KeepHighest

        return KeepHighest(self, keep=keep)  # type: ignore

    def kl(self, keep: BaseDice | int = 1) -> BaseDice:
        from .transformations import KeepLowest

        return KeepLowest(self, keep=keep)  # type: ignore

    def dh(self, drop: BaseDice | int = 1) -> BaseDice:
        from .transformations import DropHighest

        return DropHighest(self, drop=drop)  # type: ignore

    def dl(self, drop: BaseDice | int = 1) -> BaseDice:
        from .transformations import DropLowest

        return DropLowest(self, drop=drop)  # type: ignore

    @property
    def r(self):
        return self.reroll()

    def reroll(self, reroll_limit: int = 1):
        from .reroll import _RerollFactory

        return _RerollFactory(dice=self, reroll_limit=reroll_limit)

    @property
    def x(self):
        return self.explode()

    def explode(self, explode_depth: int = 100):
        from .explode import _ExplodeFactory

        return _ExplodeFactory(dice=self, explode_depth=explode_depth)

    # Magic

    def __matmul__(self, other):
        if isinstance(other, int):
            other = Scalar(other)

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")

        return DiceMany(total=self, dice=other)

    def __rmatmul__(self, other):
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

        from .math import DiceAdd

        items = other.items if isinstance(other, DiceAdd) else [other]
        if isinstance(self, DiceAdd):
            return DiceAdd((*self.items, *items))

        return DiceAdd((self, *items))

    def __radd__(self, other):
        from .math import DiceAdd

        if isinstance(other, int):
            return DiceAdd((Scalar(other), self))

        if not isinstance(other, BaseDice):
            raise TypeError("Can only add other dices or integers")

    def __sub__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only sub other dices or integers")

        from .math import DiceSub

        items = other.items if isinstance(other, DiceSub) else [other]
        if isinstance(self, DiceSub):
            return DiceSub((*self.items, *items))
        return DiceSub((self, *items))

    def __rsub__(self, other):
        from .math import DiceSub

        if isinstance(other, int):
            return DiceSub((Scalar(other), self))
        if not isinstance(other, BaseDice):
            raise TypeError("Can only sub other dices or integers")

    def __mul__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only mul other dices or integers")

        from .math import DiceMul

        items = other.items if isinstance(other, DiceMul) else [other]
        if isinstance(self, DiceMul):
            return DiceMul((*self.items, *items))
        return DiceMul((self, *items))

    def __rmul__(self, other):
        from .math import DiceMul

        if isinstance(other, int):
            return DiceMul((Scalar(other), self))
        if not isinstance(other, BaseDice):
            raise TypeError("Can only mul other dices or integers")

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .math import DiceDiv

        items = other.items if isinstance(other, DiceDiv) else [other]
        if isinstance(self, DiceDiv):
            return DiceDiv((*self.items, *items))
        return DiceDiv((self, *items))

    def __rtruediv__(self, other):
        from .math import DiceDiv

        if isinstance(other, int):
            return DiceDiv((Scalar(other), self))
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

    __floordiv__ = __truediv__  # type: ignore
    __rfloordiv__ = __rtruediv__  # type: ignore

    def __ge__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Ge

        return Ge(dice=self, compare=other)  # type: ignore

    def __gt__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Gt

        return Gt(dice=self, compare=other)  # type: ignore

    def __le__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Le

        return Le(dice=self, compare=other)  # type: ignore

    def __lt__(self, other):
        if isinstance(other, int):
            other = Scalar(other)
        if not isinstance(other, BaseDice):
            raise TypeError("Can only div other dices or integers")

        from .compare import Lt

        return Lt(dice=self, compare=other)  # type: ignore


@dataclass(slots=True)
class Scalar(BaseDice):
    value: int

    def histogram(self) -> H:
        return H([self.value])  # type: ignore

    def __str__(self) -> str:
        return str(self.value)

    def max(self) -> int:
        return self.value

    def min(self) -> int:
        return self.value

    def generate(self, items: int) -> ArrayLike:
        return np.full(items, self.value)


@dataclass(slots=True)
class Dice(BaseDice):
    sides: int
    minimal: int = field(default=1)

    def histogram(self) -> H:
        return H(range(self.minimal, self.sides + 1))  # type: ignore

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


@dataclass(slots=True)
class RangeDice(BaseDice):
    min_value: int
    max_value: int
    step_value: int = field(default=1)

    @cached_property
    def __range(self):
        return range(self.min_value, self.max_value, self.step_value)

    def histogram(self) -> H:
        return H(list(self.__range))  # type: ignore

    def __str__(self) -> str:
        if self.step_value == 1:
            return f"rng({self.min_value},{self.max_value})"
        return f"rng({self.min_value},{self.max_value},{self.step_value})"

    def max(self) -> int:
        # Calculate the number of steps
        num_steps = (self.max_value - self.min_value - 1) // self.step_value + 1
        # Calculate the actual max value in the range
        actual_max = self.min_value + (num_steps - 1) * self.step_value
        return actual_max

    def min(self) -> int:
        return self.min_value

    def generate(self, items: int) -> ArrayLike:
        return Rng().rng.choice(self.__range, size=items, replace=True)


@dataclass(slots=True)
class DiceMany(BaseDice):
    total: BaseDice
    dice: BaseDice

    def histogram(self) -> H:
        many = expandable(lambda total, dice: total.outcome @ dice.h)
        return many(self.total.histogram(), self.dice.histogram())

    def __str__(self) -> str:
        return f"{self.total}{self.dice}"

    def max(self) -> int:
        return self.dice.max() * self.total.max()

    def min(self) -> int:
        return self.dice.min() * self.total.min()

    def generate(self, items: int) -> ArrayLike:
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
            result[mask] += self.dice.generate(num_items_this_round)  # type: ignore

        return result
