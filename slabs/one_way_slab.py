from abc import ABC, abstractmethod
from typing import Optional

from structuralcodes.materials.concrete import Concrete
from structuralcodes.materials.reinforcement import Reinforcement
from structuralcodes.sections import GenericSection

from slabs.slab import Slab


class OneWaySlab(Slab, ABC):

    @property
    @abstractmethod
    def L(self) -> float:
        pass

    @abstractmethod
    def section_at(self, _x: float) -> GenericSection:
        pass
