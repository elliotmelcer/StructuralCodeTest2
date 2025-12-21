from matplotlib import pyplot as plt

from core.analysis_core import section_methods
from _mains.testing_files.testing_hp_sections import hp_section_c1_1_sls, hp_section_c1_2_c50_sls, \
    hp_section_c1_2_c80_sls, hp_section_c1_3_sls, hp_section_c1_4_sls
from core.visualization_core.visualization import plot_cracking_moment_strain_profile

"""
This file is used for verification of the cracking moment method. 

The sections used for verification are from chapter "C.1. Vergleich der Riss- und Bruchmomente" in Loutfi (2023)
"""

# Section 1:

results_c1_1        = section_methods.calculate_cracking_moment_sls_prestressed(hp_section_c1_1_sls, n=0)
results_c1_2_c50    = section_methods.calculate_cracking_moment_sls_prestressed(hp_section_c1_2_c50_sls, n=0)
results_c1_2_c80    = section_methods.calculate_cracking_moment_sls_prestressed(hp_section_c1_2_c80_sls, n=0)
results_c1_3        = section_methods.calculate_cracking_moment_sls_prestressed(hp_section_c1_3_sls, n=0)
results_c1_4        = section_methods.calculate_cracking_moment_sls_prestressed(hp_section_c1_4_sls, n=0)

print(f"Cracking Moment Verification\n"
      f"\n"
      f"Section     Mcr [kNm]\n"
      f"1           {-results_c1_1.get("m_cr")      / 1e6:>9.2f}\n"
      f"2 (C50/60)  {-results_c1_2_c50.get("m_cr")  / 1e6:>9.2f}\n"
      f"2 (C80/90)  {-results_c1_2_c80.get("m_cr")  / 1e6:>9.2f}\n"
      f"3           {-results_c1_3.get("m_cr")      / 1e6:>9.2f}\n"
      f"4           {-results_c1_4.get("m_cr")      / 1e6:>9.2f}\n")

# Plots:

# --- cross-section ---
# plot_cross_section(hp_section_c1_1_uls, x = 0)
#
# #   - Constitutive Laws:
#
# plot_constitutive_law_concrete(get_concrete(hp_section_c1_1_uls))
# plot_constitutive_law_concrete(get_concrete(hp_section_c1_1_sls))
# plot_constitutive_law_reinforcement(get_reinforcement(hp_section_c1_1_sls)[0])
#
# #   - Section Strain Profile
plot_cracking_moment_strain_profile(hp_section_c1_1_sls, results_c1_1)
#
# # Display all plots
plt.show()

