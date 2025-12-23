from matplotlib import pyplot as plt
from structuralcodes.geometry import SurfaceGeometry, add_reinforcement
from structuralcodes.sections import GenericSection

from _mains.testing_files.testing_hp_sections import hp_section_c2_uls_x_0_00, hp_section_c2_uls_x_0_10, \
    hp_section_c2_uls_x_0_20, hp_section_c2_uls_x_0_30, hp_section_c2_uls_x_0_40, hp_section_c2_uls_x_0_50
from core.analysis_core import section_methods
from core.analysis_core.section_methods import sls_section, get_concrete, calculate_moment_curvature_sls
from core.visualization_core.visualization import plot_moment_curvature, plot_constitutive_law_concrete, \
    plot_constitutive_law_reinforcement, table_moment_curvature, plot_cross_section
from slabs.hp_shell.model.hp_shell import HPShell
from _mains.testing_files.testing_materials import solidian_Q142_pre_50, concrete_c50_uls


moment_curvature_c2_x_0_00 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_00)
moment_curvature_c2_x_0_10 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_10)
moment_curvature_c2_x_0_20 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_20)
moment_curvature_c2_x_0_30 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_30)
moment_curvature_c2_x_0_40 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_40)
moment_curvature_c2_x_0_50 = calculate_moment_curvature_sls(hp_section_c2_uls_x_0_50)

# --- M-K-results_c2 ---

# print
plot_moment_curvature(moment_curvature_c2_x_0_00, x = 0.00)
plot_moment_curvature(moment_curvature_c2_x_0_10, x = 0.10)
plot_moment_curvature(moment_curvature_c2_x_0_20, x = 0.20)
plot_moment_curvature(moment_curvature_c2_x_0_30, x = 0.30)
plot_moment_curvature(moment_curvature_c2_x_0_40, x = 0.40)
plot_moment_curvature(moment_curvature_c2_x_0_50, x = 0.50)

# table
# print(table_moment_curvature(moment_curvature_c2))

# --- show ---
plt.show()

