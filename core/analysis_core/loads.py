import numpy as np

class Loads:

    """
    Class for instantiating a load model according to Eurocode 0
    """

    def __init__(
        self,
        load_values,
        gamma_values,
        psi_0_values,
        psi_1_values,
        psi_2_values
    ):
        self.load_values = np.array(load_values, dtype=float)
        self.gamma_values = np.array(gamma_values, dtype=float)
        self.psi_0_values = np.array(psi_0_values, dtype=float)
        self.psi_1_values = np.array(psi_1_values, dtype=float)
        self.psi_2_values = np.array(psi_2_values, dtype=float)

        self._check_dimensions()

    def _check_dimensions(self):
        n = len(self.load_values)
        for arr in [
            self.gamma_values,
            self.psi_0_values,
            self.psi_1_values,
            self.psi_2_values,
        ]:
            if len(arr) != n:
                raise ValueError("All input arrays must have the same length")

    def fundamental_combination(self):
        """
        Ultimate Limit State (ULS)
        EC0 6.10
        """
        return np.sum(
            self.gamma_values * self.load_values * self.psi_0_values
        )

    def frequent_combination(self):
        """
        Serviceability Limit State (SLS) – frequent combination
        EC0 6.15b
        """
        return np.sum(
            self.load_values * self.psi_1_values
        )

    def permanent_combination(self):
        """
        Serviceability Limit State (SLS) – quasi-permanent combination
        EC0 6.16b
        """
        return np.sum(
            self.load_values * self.psi_2_values
        )
