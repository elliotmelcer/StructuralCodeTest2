from _mains.testing_files.testing_floor import test_floor
from _mains.testing_files.testing_hp_sections import hp_c1_4
from _mains.testing_files.testing_slab_construction import test_slab_construction
from core.analysis_core.loads import Loads
from slab_construction.slab_construction import SlabConstruction

slab_construction = SlabConstruction(hp_c1_4, test_floor)

live_loads = [3.0] #kN/m²

psi_0_values = [1.0]
psi_1_values = [1.0]
psi_2_values = [0.3]

test_loads = Loads(test_slab_construction, live_loads, psi_0_values, psi_1_values, psi_2_values)