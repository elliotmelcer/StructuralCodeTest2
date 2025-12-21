from core.analysis_core import section_methods

from _mains.testing_files.testing_hp_sections import hp_section_c1_1_sls, hp_section_c1_2_c50_sls, \
    hp_section_c1_2_c80_sls, hp_section_c1_3_sls, hp_section_c1_4_sls

"""
This file is used for verification of the cracking moment method. 

The sections used for verification are from chapter "C.1. Vergleich der Riss- und Bruchmomente" in Loutfi (2023)
"""

# Section 1:

mu_sls_c1_1        = hp_section_c1_1_sls.section_calculator.calculate_bending_strength().m_y
mu_sls_c1_2_c50    = hp_section_c1_2_c50_sls.section_calculator.calculate_bending_strength().m_y
mu_sls_c1_2_c80    = hp_section_c1_2_c80_sls.section_calculator.calculate_bending_strength().m_y
mu_sls_c1_3        = hp_section_c1_3_sls.section_calculator.calculate_bending_strength().m_y
mu_sls_c1_4        = hp_section_c1_4_sls.section_calculator.calculate_bending_strength().m_y

print(f"Ultimate Moment (sls) Verification\n"
      f"\n"
      f"Section     Mu [kNm]\n"
      f"1           {-mu_sls_c1_1      / 1e6:>9.2f}\n"
      f"2 (C50/60)  {-mu_sls_c1_2_c50  / 1e6:>9.2f}\n"
      f"2 (C80/90)  {-mu_sls_c1_2_c80  / 1e6:>9.2f}\n"
      f"3           {-mu_sls_c1_3       / 1e6:>9.2f}\n"
      f"4           {-mu_sls_c1_4      / 1e6:>9.2f}\n")