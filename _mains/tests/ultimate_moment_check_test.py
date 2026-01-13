from _mains.testing_files.testing_loads import test_loads
from core.analysis_core.checks.check import UltimateMomentCheckEC2004DE

print(f"{UltimateMomentCheckEC2004DE.calculateUtilization(test_loads):.3f}")