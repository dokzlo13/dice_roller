import numpy as np


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


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
