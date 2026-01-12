import numpy as np

from core.analysis_core.loads import Loads
from core.unit_core import mm_to_m


class InternalForces:
    """
    Author: Elliot Melcer

    Utility class (not instantiable) providing methods to compute internal forces
    for a simply supported beam under uniform distributed load.
    """

    @staticmethod
    def moment_simple_beam(loads: Loads, combination: str = "FUNDAMENTAL") -> float:
        """
        Returns the Moment in [kNm] given
        :param loads:
        :param combination:
        :return:
        """
        span = mm_to_m(loads.slab_construction.slab.L)
        width = mm_to_m(loads.slab_construction.slab.B)

        # for easier user behavior: accepts "FUNDAMENTAL", "fundamental" or "  Fundamental  "
        combination = combination.strip().upper()

        if combination == "FUNDAMENTAL":
            w = loads.fundamental_combination()  # kN/m²
        elif combination == "FREQUENT":
            w = loads.frequent_combination()  # kN/m²
        elif combination in ("QUASI-PERMANENT", "QUASI_PERMANENT", "QUASI PERMANENT"):
            w = loads.quasi_permanent_combination()  # kN/m²
        else:
            raise ValueError(
                "Invalid combination. Must be one of: 'FUNDAMENTAL', 'FREQUENT', 'QUASI-PERMANENT'."
            )

        # Convert surface load [kN/m²] to line load [kN/m] using slab width
        w_line = w * width

        # Simply supported beam under UDL: Mmax = w*L^2/8
        return w_line * span**2 / 8.0

