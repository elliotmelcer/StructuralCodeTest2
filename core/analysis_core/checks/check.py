from abc import ABC, abstractmethod

from core.analysis_core.internal_forces import InternalForces
from core.analysis_core.loads import Loads
from core.analysis_core.section_methods import calculate_bending_strength_uls
from core.unit_core import Nmm_to_kNm


class StructuralCheck(ABC):
    def __init__(self, name: str, loads: Loads):
        self.name = name
        self.loads = loads

    @abstractmethod
    def calculateUtilization(self) -> float:
        """
        Returns the utilization ratio
        """
        raise NotImplementedError


class UltimateMomentCheckEC2004DE(StructuralCheck):
    def __init__(self, loads: Loads) -> None:
        super().__init__("ULS bending moment", loads)

    def calculateUtilization(self) -> float:
        slab = self.loads.slab_construction.slab

        MRd = Nmm_to_kNm(calculate_bending_strength_uls(slab.section_at(0.0)).get('m_u'))

        MEd = InternalForces.moment_simple_beam(self.loads, "FUNDAMENTAL")

        return MEd / MRd
