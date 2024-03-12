from . import random
from .callback import WithGenerateCallback, WithRollCallback
from .compare import Ge, Gt, Le, Lt, Limit
from .core import (
    BaseDice,
    Dice,
    DiceMany,
    RangeDice,
    Scalar,
)
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
