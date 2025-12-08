from matplotlib import pyplot as plt
from structuralcodes.geometry import SurfaceGeometry, add_reinforcement
from structuralcodes.sections import GenericSection

from core.visualization_core.visualization import plot_moment_curvature, plot_constitutive_law_concrete, \
    plot_constitutive_law_reinforcement, table_moment_curvature, plot_cross_section
from slabs.hp_shell.model.hp_shell import HPShell
from testing_generics import generic_cfrp_pre, generic_concrete_c50, \
    generic_cfrp

# hp_geometry stuff
b  = 1200      #mm
l = 6750      #mm
hx = 70        # mm
hy = 280       #mm
t   = 40        #mm
dy = 30         #mm
nt = 5          #-

x = 0.5 * l

hp = HPShell(B = b, L = l, Hx = hx, Hy = hy, t = t, dy = dy, nt = nt)

# structural codes stuff

# --- concrete section ---
hp_geometry = SurfaceGeometry(
    poly=hp.polygon_section(x = x, n = 100), material=generic_concrete_c50
)

# --- reinforcement ---
reinforcement_points = hp.tendon_coords_at_x(x = x)

for pt in reinforcement_points:
    hp_geometry = add_reinforcement(
        hp_geometry,
        pt,       # reinforcement points
        3.56825,        # diameter [mm]
        generic_cfrp_pre  # reinforcement material
    )

hp_section = GenericSection(hp_geometry)
moment_curvature = hp_section.section_calculator.calculate_moment_curvature()

print(hp_section.section_calculator.calculate_cracking_moment(n=0))

# # --- constitutive laws ---
#
# # prints
# print('Beton Arbeitslinie: ', generic_concrete_c50.constitutive_law)
# print('CFK Arbeitslinie: ', generic_cfrp.constitutive_law)
#
# # plots
# plot_constitutive_law_concrete(generic_concrete_c50)
# plot_constitutive_law_reinforcement(generic_cfrp_pre)
#
# # --- cross-section ---
# plot_cross_section(hp_section, x = x/l)
#
#
# # --- M-K-results ---
#
# # print
# plot_moment_curvature(moment_curvature, x = x/l)
#
# # table
# print(table_moment_curvature(moment_curvature))
#
# # --- show ---
# plt.show()

