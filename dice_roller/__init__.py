from . import random
from .callback import WithGenerateCallback, WithRollCallback
from .compare import Ge, Gt, Le, Limit, Lt
from .core import BaseDice, Dice, DiceMany, RangeDice, Scalar, many
from .explode import Explode
from .math import (
    DiceAdd,
    DiceDiv,
    DiceMul,
    DiceSub,
)
from .reroll import Reroll
from .transformations import DropHighest, DropLowest, KeepHighest, KeepLowest

s = Scalar
d = Dice
kh = KeepHighest
kl = KeepLowest
dh = DropHighest
dl = DropLowest
x = Explode
r = Reroll
rng = RangeDice
lim = Limit


__all__ = [
    "random",
    "WithGenerateCallback",
    "WithRollCallback",
    "Ge",
    "Gt",
    "Le",
    "Limit",
    "Lt",
    "BaseDice",
    "Dice",
    "DiceMany",
    "RangeDice",
    "Scalar",
    "many",
    "Explode",
    "DiceAdd",
    "DiceDiv",
    "DiceMul",
    "DiceSub",
    "Reroll",
    "DropHighest",
    "DropLowest",
    "KeepHighest",
    "KeepLowest",
    "s",
    "d",
    "kh",
    "kl",
    "dh",
    "dl",
    "x",
    "r",
    "rng",
    "lim",
]
