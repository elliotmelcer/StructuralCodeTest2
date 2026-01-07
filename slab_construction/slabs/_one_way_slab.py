from abc import ABC, abstractmethod

from structuralcodes.sections import GenericSection

from slab_construction.slabs.slab import Slab


class OneWaySlab(Slab, ABC):

    @property
    @abstractmethod
    def L(self) -> float:
        pass

    @abstractmethod
    def section_at(self, _x: float) -> GenericSection:
        pass
