import numpy as np

class Loads:

    """
    Author: Elliot Melcer
    Class for instantiating a load model according to Eurocode 0
    """

    def __init__(
        self,
        slab_construction,
        live_loads,
        psi_0_values,
        psi_1_values,
        psi_2_values,
        gamma_g = 1.35,
        gamma_q = 1.5,
    ):

        self.Qk = np.array(live_loads, dtype=float)
        self.slab_construction = slab_construction
        self.psi_0_values = np.array(psi_0_values, dtype=float)
        self.psi_1_values = np.array(psi_1_values, dtype=float)
        self.psi_2_values = np.array(psi_2_values, dtype=float)
        self.gamma_g = gamma_g
        self.gamma_q = gamma_q
        self._check_dimensions()

    # --- Permanent actions from SlabConstruction ---
    @property
    def Gk_struct(self) -> float:
        return float(self.slab_construction.structural_dead_load())

    @property
    def Gk_non_struct(self) -> float:
        return float(self.slab_construction.non_structural_dead_load())

    def _check_dimensions(self) -> None:
        """
        Checks the dimension compatibility of the input.
        """
        n = len(self.Qk)
        for arr in [self.psi_0_values, self.psi_1_values, self.psi_2_values]:
            if len(arr) != n:
                raise ValueError("All live load (Qk) and psi arrays must have the same length")

    def fundamental_combination(self):
        """
        Ultimate Limit State (ULS) - fundamental combination
        EC0 6.10
        """
        Gd = self.gamma_g * (self.Gk_struct + self.Gk_non_struct)
        Qd = self.gamma_q * float(np.sum(self.Qk * self.psi_0_values))

        return Gd + Qd

    def frequent_combination(self):
        """
        Serviceability Limit State (SLS) – frequent combination
        EC0 6.15b
        """
        return self.Gk_struct + self.Gk_non_struct + float(np.sum(self.Qk * self.psi_1_values))

    def quasi_permanent_combination(self):
        """
        Serviceability Limit State (SLS) – quasi-permanent combination
        EC0 6.16b
        """
        return self.Gk_struct + self.Gk_non_struct + float(np.sum(self.Qk * self.psi_2_values))
