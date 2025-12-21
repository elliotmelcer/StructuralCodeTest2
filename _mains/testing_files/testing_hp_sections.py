from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from structuralcodes.geometry import SurfaceGeometry, add_reinforcement
from structuralcodes.materials.concrete import Concrete
from structuralcodes.materials.reinforcement import Reinforcement
from structuralcodes.sections import GenericSection
from core.analysis_core.section_methods import sls_section
from core.visualization_core.visualization import plot_cross_section
from slabs.hp_shell.model.hp_shell import HPShell
from _mains.testing_files.testing_materials import concrete_c50_uls, solidian_Q142_pre_50, \
    concrete_c80_uls, solidian_Q142, solidian_Q95_pre_50, solidian_Q95_pre_20, solidian_Q142_pre_60, concrete_c55_uls


def make_section(hp: HPShell, conc: Concrete, reinforcement: Reinforcement, reinf_area: float, _x: float, name: Optional[str] = None) -> GenericSection:
    """
    Author: Elliot Melcer
    Returns a section from a hp-shell, material properties, reinforcement area and location in shell

    Note:
        Reinforcement Area in mm²
        x in mm
    """
    # Concrete Geometry
    hp_geometry = SurfaceGeometry(
        poly=hp.polygon_section(x=_x, n=100), material=conc
    )

    # Reinforcement Geometry
    reinforcement_points = hp.tendon_coords_at_x(x=_x)
    d = np.sqrt(4 * reinf_area / np.pi)

    # Add Reinforcement to Concrete Geometry
    for pt in reinforcement_points:
        hp_geometry = add_reinforcement(
            hp_geometry,
            pt,  # reinforcement points
            d,  # diameter [mm]
            reinforcement  # reinforcement material
        )

    if name is None:
        hp_section = GenericSection(hp_geometry)
    else:
        hp_section = GenericSection(hp_geometry, name = name)

    return hp_section

"""
Author: Elliot Melcer

HP-Shells for Testing. Naming convention after:

    Jamila Loutfi (2023):   "Entwicklung eines parametrischen Bemessungsmodells 
                            für ein Deckensystem aus vorgespannten doppelt-gekrümmten 
                            Schalen aus Carbonbeton"
                            
"""

# --- HP Shells for Verification of Cracking and Ultimate Moments---

x = 0.0 # Location of Section in Girder

# HP Shell Geometries

# Note: Hx was determined through trial and error, since it was not provided in Loutfi (2023)
hp_c1_1 = HPShell(B = 1200, L = 6750, Hx = 40, Hy = 160, t = 40,  dy = 100, nt = 7)
hp_c1_2 = HPShell(B = 1200, L = 6750, Hx = 75, Hy = 300, t = 70,  dy = 50,  nt = 8)
hp_c1_3 = HPShell(B = 1500, L = 6750, Hx = 125, Hy = 500, t = 50,  dy = 50,  nt = 1)
hp_c1_4 = HPShell(B = 1200, L = 6750, Hx = 100, Hy = 400, t = 100, dy = 80,  nt = 10)

# ULS Sections
hp_section_c1_1_uls     = make_section(hp_c1_1, concrete_c50_uls, solidian_Q95_pre_20 , reinf_area = 50,  _x = x * hp_c1_1.L, name = "C.1. Section 1")
hp_section_c1_2_c50_uls = make_section(hp_c1_2, concrete_c50_uls, solidian_Q95_pre_50 , reinf_area = 50,  _x = x * hp_c1_2.L, name = "C.1. Section 2.1")
hp_section_c1_2_c80_uls = make_section(hp_c1_2, concrete_c80_uls, solidian_Q95_pre_50 , reinf_area = 50,  _x = x * hp_c1_2.L, name = "C.1. Section 2.2")
hp_section_c1_3_uls     = make_section(hp_c1_3, concrete_c50_uls, solidian_Q142       , reinf_area = 300, _x = x * hp_c1_3.L, name = "C.1. Section 3")
hp_section_c1_4_uls     = make_section(hp_c1_4, concrete_c55_uls, solidian_Q142_pre_50, reinf_area = 80,  _x = x * hp_c1_4.L, name = "C.1. Section 4")

# SLS Sections
hp_section_c1_1_sls     = sls_section(hp_section_c1_1_uls)
hp_section_c1_2_c50_sls = sls_section(hp_section_c1_2_c50_uls)
hp_section_c1_2_c80_sls = sls_section(hp_section_c1_2_c80_uls)
hp_section_c1_3_sls     = sls_section(hp_section_c1_3_uls)
hp_section_c1_4_sls     = sls_section(hp_section_c1_4_uls)


# --- HP Shell for Verification of Moment-Curvature-Diagram ---
hp_c2 = HPShell(B = 1200, L = 6750, Hx = 70, Hy = 280, t = 40, dy = 30, nt = 5)

hp_section_c2 = make_section(hp_c2, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10,  _x = x * hp_c2.L, name = "C.2. Section")



if __name__ == "__main__":
    plot_cross_section(hp_section_c1_1_uls)
    plot_cross_section(hp_section_c1_2_c50_uls)
    plot_cross_section(hp_section_c1_2_c80_uls)
    plot_cross_section(hp_section_c1_3_uls)
    plot_cross_section(hp_section_c1_4_uls)

    plot_cross_section(hp_section_c2)

    plt.show()



