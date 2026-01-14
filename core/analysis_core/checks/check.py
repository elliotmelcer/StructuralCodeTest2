from abc import ABC, abstractmethod

from core.analysis_core.statics.internal_forces import InternalForces
from core.analysis_core.loads import Loads
from core.analysis_core.section_methods import calculate_bending_strength_uls
from core.unit_core import Nmm_to_kNm
from slab_construction.slab_construction import SlabConstruction


class StructuralCheck(ABC):

    @staticmethod
    @abstractmethod
    def calculateUtilization(
            slab_construction: SlabConstruction,
            loads: Loads,
            system: str,
            moment: str) -> float:
        """Returns the utilization ratio"""
        raise NotImplementedError


class UltimateMomentCheckEC2004DE(StructuralCheck):

    @staticmethod
    def calculateUtilization(
            slab_construction: SlabConstruction,
            loads: Loads,
            system: str = "SIMPLE_BEAM",
            moment: str = "MAX_POS_MOMENT"
    ) -> float:
        """
        Calculate utilization ratio for ultimate moment check

        :param slab_construction: Slab construction object
        :param loads: Loads object (only uniformly distributed loads over all spans)
        :param system: Available structural system types:
                            ("CANTILEVER",
                            "SIMPLE_BEAM",
                            "TWO_SPAN",
                            "THREE_SPAN",
                            "FOUR_SPAN" or
                            "FIVE_SPAN")
        :param moment: Moment type
                            ("MAX_POS_MOMENT" or
                            "MAX_NEG_MOMENT")
        :return: Utilization ratio (MEd/MRd)
        """
        slab = slab_construction.slab

        # Normalize inputs
        system = system.strip().upper()
        moment = moment.strip().upper()

        # Get moment data (coefficient and x-position) from lookup table
        moment_data = InternalForces.get_moment_data(system, moment)
        x_position = moment_data["x_position"]

        # Validate x-position is within bounds for this system
        InternalForces.validate_x_position(system, x_position)

        # Calculate resistance at the specific x-position where max moment occurs
        # x_position is normalized (0 at first support, 1 at second support, etc.)
        # Must Do: Catch Stützmoment Fall (Achtung anderes MRd, Querschnitt umdrehen?)
        MRd = -Nmm_to_kNm(
            calculate_bending_strength_uls(slab.section_at(x_position)).get("m_u")
        )

        print(f"System: {system}, Moment Type: {moment}")
        print(f"x-position: {x_position}")
        print(f"M_Rd = {MRd:.3f} kNm")

        # Calculate design moment based on system and moment type
        MEd = InternalForces.calculate_moment(slab_construction, loads, system, moment, "FUNDAMENTAL")

        print(f"M_Ed = {MEd:.3f} kNm")

        # Calculate utilization
        utilization = abs(MEd / MRd)

        print(f"Utilization = {utilization:.3f} ({utilization * 100:.1f}%)")

        return utilization