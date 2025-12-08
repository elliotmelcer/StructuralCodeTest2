# Create a concrete and a reinforcement
from scipy.ndimage import generic_filter
from structuralcodes import set_design_code
from structuralcodes.materials.concrete import create_concrete, ConcreteEC2_2023
from structuralcodes.materials.concrete import _concreteEC2_2023
from structuralcodes.materials.constitutive_laws import InitialStrain, create_constitutive_law, Elastic, BilinearCompression
from structuralcodes.materials.reinforcement import create_reinforcement, ReinforcementEC2_2023

set_design_code('ec2_2004')

# --- Material Properties ---

# concrete
fck_45 = 45
fck_50 = 50

# steel reinforcemenet
fyk_b500 = 500
ftk_b500 = 550
Es_b500 = 200000
epsuk_b500 = 0.07



# --- Material Definitions ---

# concrete
generic_concrete_c50= create_concrete(fck=fck_50, constitutive_law = 'parabolarectangle')

# steel reinforcement
generic_reinforcement = create_reinforcement(fyk=fyk_b500, Es=Es_b500, ftk=ftk_b500, epsuk=epsuk_b500, density=7850, constitutive_law="elasticperfectlyplastic")

# cfrp reinforcement
fyk_cfrp = 2199.99999
ftk_cfrp = 2200
Es_cfrp = 220_000
epsuk_cfrp = 0.01
density_cfrp = 1800
initial_strain_cfrp = 0.6


# constitutive law for cfrp reinforcement
brittle_elastic_law = Elastic(Es_cfrp)
brittle_elastic_law.set_ultimate_strain(epsuk_cfrp)

# prestressed cfrp reinforcement
generic_cfrp_pre = create_reinforcement(
    fyk=fyk_cfrp,
    Es=Es_cfrp,
    ftk=ftk_cfrp,
    epsuk=epsuk_cfrp,
    density=density_cfrp,
    constitutive_law=brittle_elastic_law,
    initial_strain =initial_strain_cfrp * epsuk_cfrp
)

# cfrp reinforcement

generic_cfrp = create_reinforcement(
    fyk=fyk_cfrp,
    Es=Es_cfrp,
    ftk=ftk_cfrp,
    epsuk=epsuk_cfrp,
    density=density_cfrp,
    constitutive_law=brittle_elastic_law
)
