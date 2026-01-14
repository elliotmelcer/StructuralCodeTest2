from abc import ABC, abstractmethod

from core.analysis_core.internal_forces import InternalForces
from core.analysis_core.loads import Loads
from core.analysis_core.section_methods import calculate_bending_strength_uls
from core.unit_core import Nmm_to_kNm
from slab_construction.slab_construction import SlabConstruction


class StructuralCheck(ABC):

    @staticmethod
    @abstractmethod
    def calculateUtilization(slab_construction: SlabConstruction, loads: Loads, system: str, moment: str) -> float:
        """Returns the utilization ratio"""
        raise NotImplementedError


class UltimateMomentCheckEC2004DE(StructuralCheck):

    @staticmethod
    def calculateUtilization(slab_construction: SlabConstruction, loads: Loads, system: str = "SIMPLE_BEAM", moment: str = "MAX_POS_MOMENT") -> float:
        slab = loads.slab_construction.slab

        MRd = - Nmm_to_kNm(
            calculate_bending_strength_uls(slab.section_at(0.0)).get("m_u")
        )

        print(f"M_Rd = {MRd:.3f}")

        MEd = InternalForces.moment_simple_beam(loads, "FUNDAMENTAL")

        print(f"MEd = {MEd:.3f}")

        return MEd / MRd
