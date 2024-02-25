import numpy as np

from .misc import SingletonMeta


class Rng(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._rng: np.random.Generator = None  # type: ignore

    @property
    def rng(self) -> np.random.Generator:
        if self._rng is None:
            raise RuntimeError("No RNG generator ")
        return self._rng

    def set_rng(self, rng: np.random.Generator):
        self._rng = rng


Rng().set_rng(np.random.default_rng())
