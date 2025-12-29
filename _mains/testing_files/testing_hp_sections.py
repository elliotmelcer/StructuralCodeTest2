from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from structuralcodes.geometry import SurfaceGeometry, add_reinforcement
from structuralcodes.materials.concrete import Concrete
from structuralcodes.materials.reinforcement import Reinforcement
from structuralcodes.sections import GenericSection
from core.visualization_core.visualization import plot_cross_section
from slabs.hp_slab.model.hp_slab import HPSlab
from _mains.testing_files.testing_materials import concrete_c50_uls, solidian_Q142_pre_50, \
    concrete_c80_uls, solidian_Q142, solidian_Q95_pre_50, solidian_Q95_pre_20, solidian_Q142_pre_60, concrete_c55_uls




"""
Author: Elliot Melcer

HP-Shells for Testing. Naming convention after:

    Jamila Loutfi (2023):   "Entwicklung eines parametrischen Bemessungsmodells 
                            für ein Deckensystem aus vorgespannten doppelt-gekrümmten 
                            Schalen aus Carbonbeton"
                            
"""

def make_section(hp: HPSlab, conc: Concrete, reinforcement: Reinforcement, reinf_area: float, _x: float, name: Optional[str] = None) -> GenericSection:
    """
    Author: Elliot Melcer
    Returns a section from a hp-shell, material properties, reinforcement area and location in shell

    Note:
        Reinforcement Area in mm²
        x in mm
    """
    # Concrete Geometry
    hp_geometry = SurfaceGeometry(
        poly=hp.polygon_section_at(x=_x, n=100), material=conc
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


# --- HP Shells for Verification of Cracking and Ultimate Moments---

x = 0.0 # Location of Section in Girder

# HP Shell Geometries

# Note: Hx was determined through trial and error, since it was not provided in Loutfi (2023)
hp_c1_1 = HPSlab(B = 1200, L = 6750, Hx = 40, Hy = 160, t = 40, dy = 100, nt = 7)
hp_c1_2 = HPSlab(B = 1200, L = 6750, Hx = 75, Hy = 300, t = 70, dy = 50, nt = 8)
hp_c1_3 = HPSlab(B = 1500, L = 6750, Hx = 125, Hy = 500, t = 50, dy = 50, nt = 1)
hp_c1_4 = HPSlab(B = 1200, L = 6750, Hx = 100, Hy = 400, t = 100, dy = 80, nt = 10)

# ULS Sections
hp_section_c1_1_uls     = hp_c1_1.section_at(x, concrete_c50_uls, solidian_Q95_pre_20 , reinf_area = 50,   name = "C.1. Section 1")
hp_section_c1_2_c50_uls = hp_c1_2.section_at(x, concrete_c50_uls, solidian_Q95_pre_50 , reinf_area = 50,  name = "C.1. Section 2.1")
hp_section_c1_2_c80_uls = hp_c1_2.section_at(x, concrete_c80_uls, solidian_Q95_pre_50 , reinf_area = 50,  name = "C.1. Section 2.2")
hp_section_c1_3_uls     = hp_c1_3.section_at(x, concrete_c50_uls, solidian_Q142       , reinf_area = 300, name = "C.1. Section 3")
hp_section_c1_4_uls     = hp_c1_4.section_at(x, concrete_c55_uls, solidian_Q142_pre_50, reinf_area = 80,  name = "C.1. Section 4")


# --- HP Shell for Verification of Moment-Curvature-Diagram ---
hp_c2 = HPSlab(B = 1200, L = 6750, Hx = 70, Hy = 280, t = 40, dy = 30, nt = 5)

# ULS Sections
hp_section_c2_uls_x_0_00 = hp_c2.section_at(0.00, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.00 * L")
hp_section_c2_uls_x_0_10 = hp_c2.section_at(0.10, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.10 * L")
hp_section_c2_uls_x_0_20 = hp_c2.section_at(0.20, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.20 * L")
hp_section_c2_uls_x_0_30 = hp_c2.section_at(0.30, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.30 * L")
hp_section_c2_uls_x_0_40 = hp_c2.section_at(0.40, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.40 * L")
hp_section_c2_uls_x_0_50 = hp_c2.section_at(0.50, concrete_c50_uls, solidian_Q142_pre_60, reinf_area = 10, name = "C.2. Section at 0.50 * L")


if __name__ == "__main__":
    plot_cross_section(hp_section_c1_1_uls)
    plot_cross_section(hp_section_c1_2_c50_uls)
    plot_cross_section(hp_section_c1_2_c80_uls)
    plot_cross_section(hp_section_c1_3_uls)
    plot_cross_section(hp_section_c1_4_uls)

    plot_cross_section(hp_section_c2_uls_x_0_00)

    plt.show()



