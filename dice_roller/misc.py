from .core import BaseDice, Scalar
from typing import Callable


def _wrap_scalar(value: BaseDice | int) -> BaseDice:
    if isinstance(value, int):
        value = Scalar(value)
    if not isinstance(value, BaseDice):
        raise TypeError("Reroll only support other dices or integers")
    return value


DiceModifier = Callable[[BaseDice], BaseDice]
