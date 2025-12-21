import numpy as np
from structuralcodes.geometry import  CompoundGeometry, SurfaceGeometry
from structuralcodes.materials.concrete import Concrete, create_concrete
from structuralcodes.materials.reinforcement import Reinforcement
from structuralcodes.sections import GenericSection

'''
def calculate_cracking_moment(section: GenericSection, n: float) -> float:
    """
    Author: Elliot Melcer
    Global function computing cracking moment of a GenericSection
    under axial force n.
    """
    # --- Material Properties ---
    conc = get_concrete(section)

    # Secant Modulus of Concrete at eps = 0
    E = conc.constitutive_law.get_secant(0)
    Ecm = conc.Ecm
    print("E-Secant (ULS) = ", E, " N/mm^2")
    print("Ecm (ULS) = ", Ecm, " N/mm^2")

    # Tensile Strength
    conc = get_concrete(section)
    fctm = conc.fctm


    # --- Geometric Properties ---
    gross_props = section.gross_properties

    cz = gross_props.cz
    e_iyy_c = gross_props.e_iyy_c
    ea = gross_props.ea

    iyy_hom = e_iyy_c / E

    _, _, zmin, _ = section.geometry.calculate_extents()
    z_t = zmin - cz        # centroid to bottom fibre
    wy = iyy_hom / z_t         # section modulus


    # Count reinforcement bars
    n_reinf = get_number_of_reinforcements(section)

    # reinforcement, area = get_reinforcement(section)
    # eps_ini = reinforcement.initial_strain
    # if eps_ini is None:
    #     eps_ini = 0.0
    # E_s = reinforcement.Es
    # a_s = area

    # --- Calculations ---
    # p = eps_ini * E_s * a_s

    # m_cr = wy * (fctm - n_reinf * p / a)
    m_cr = wy * fctm

    # --- Print ---
    print(f"Method: calculate_cracking_moment \n"
          f"Calculation: f_ctm={fctm:.2f} MPa, "
          f"EA={ea:.3e} N, "
          f"EI_yy_c={e_iyy_c:.2e} Nmm^2, "
          f"I_yy_hom={iyy_hom:.2e} mm^4, "
          f"cz={cz:.2e} mm, "
          f"distance centroid to bottom fiber={z_t:.2e} mm, "
          f"W_y={wy:.2e} mm³, "
          f"M_cr={m_cr:.2e} Nmm")

    return m_cr
'''


def calculate_cracking_moment_sls(section: GenericSection, n: float) -> float:
    """
    Author: Elliot Melcer
    Global function computing cracking moment of a GenericSection
    under axial force n.
    """
    sls_sec = sls_section(section)

    # --- Material Properties ---
    conc = get_concrete(sls_sec)

    # Secant Modulus of Concrete at eps = 0
    E = conc.constitutive_law.get_secant(0)
    Ecm = conc.Ecm
    print("E-Secant (SLS) = ", E, " N/mm^2")
    print("Ecm (SLS) = ", Ecm, " N/mm^2")

    # Tensile Strength
    conc = get_concrete(sls_sec)
    fctm = conc.fctm


    # --- Geometric Properties ---
    gross_props = sls_sec.gross_properties

    cz = gross_props.cz
    e_iyy_c = gross_props.e_iyy_c
    ea = gross_props.ea
    a_sec = gross_props.area

    iyy_hom = e_iyy_c / E

    _, _, zmin, _ = sls_sec.geometry.calculate_extents()
    z_t = zmin - cz        # centroid to bottom fibre
    wy = iyy_hom / z_t         # section modulus


    # Count reinforcement bars
    n_reinf = get_number_of_reinforcements(section)

    reinforcement, area = get_reinforcement(section)
    eps_ini = reinforcement.initial_strain
    if eps_ini is None:
        eps_ini = 0.0
    E_s = reinforcement.Es
    a_s = area

    # --- Calculations ---
    p = -eps_ini * E_s * a_s

    # m_cr = wy * (fctm - n_reinf * p / a_sec)
    m_cr = wy * fctm

    # --- Print ---
    print(f"Method: calculate_cracking_moment (SLS)\n"
          f"Calculation: f_ctm={fctm:.2f} MPa, "
          f"EA={ea:.3e} N, "
          f"EI_yy_c={e_iyy_c:.2e} Nmm^2, "
          f"I_yy_hom={iyy_hom:.2e} mm^4, "
          f"cz={cz:.2e} mm, "
          f"distance centroid to bottom fiber={z_t:.2e} mm, "
          f"W_y={wy:.2e} mm³, "
          f"M_cr={m_cr:.2e} Nmm")

    return m_cr


def calculate_cracking_moment_sls_prestressed(section: GenericSection, n: float = 0.0) -> dict:
    """
    Author: Elliot Melcer
    Calculate cracking moment of a prestressed GenericSection.

    The function finds the strain profile where the bottom fiber reaches
    the cracking strain eps_ctm = fctm / Ecm, while maintaining equilibrium
    with the applied axial force n.

    Args:
        section: GenericSection object (should be SLS section)
        n: Applied axial force (positive = tension, negative = compression)

    Returns:
        dict: Dictionary containing:
            - m_cr: Cracking moment (Nmm)
            - strain_profile: [eps_0, chi_y, chi_z] at cracking
            - reinforcement_strains: List of strains in each reinforcement
            - stress_resultants: [N, My, Mz] at cracking
    """

    # --- Concrete Properties ---
    # Find concrete geometry (assume first surface geometry with concrete)
    conc = None
    for geo in section.geometry.geometries:
        if hasattr(geo, 'concrete') and geo.concrete:
            conc = geo.material
            break

    if conc is None:
        raise ValueError("No concrete geometry found in section")

    # Get concrete properties
    Ecm = conc.Ecm
    fctm = conc.fctm
    eps_ctm = fctm / Ecm  # Cracking strain

    # print(f"Ecm = {Ecm:.2f} N/mm²")
    # print(f"fctm = {fctm:.2f} N/mm²")
    # print(f"eps_ctm = {eps_ctm:.6f}")

    # --- Geometric Section Properties ---
    gross_props = section.gross_properties

    # Centroid z-coordinate
    cz = gross_props.cz

    # Get section extents
    _, _, zmin, zmax = section.geometry.calculate_extents()
    # print(f"Section extents: zmin = {zmin:.2f} mm, zmax = {zmax:.2f} mm")
    # print(f"Centroid cz = {cz:.2f} mm")

    # --- Get Reinforcement Properties ---
    point_geometries = section.geometry.point_geometries
    n_reinf = len(point_geometries)

    if n_reinf == 0:
        print("Warning: No reinforcement found in section")

    # Extract reinforcement data
    z_reinforcements = []
    eps_ini_list = []
    E_s_list = []
    a_s_list = []

    for pg in point_geometries:
        z_reinforcements.append(pg.point.y)  # z-coordinate

        # Initial strain (prestress)
        eps_ini = pg.material.initial_strain if hasattr(pg.material, 'initial_strain') else 0.0
        if eps_ini is None:
            eps_ini = 0.0
        eps_ini_list.append(eps_ini)

        # Material properties
        E_s = pg.material.Es if hasattr(pg.material, 'Es') else pg.material.constitutive_law.get_tangent(0)
        E_s_list.append(E_s)

        # Area
        a_s_list.append(pg.area)

    # print(f"\nNumber of reinforcements: {n_reinf}")
    # if n_reinf > 0:
    #     print(f"Reinforcement z-coordinates: {z_reinforcements}")
        # print(f"Initial strains: {eps_ini_list}")

    # --- Find Strain Profile at Cracking ---
    # At cracking, the bottom fiber has strain eps_ctm
    # Strain profile: eps(z) = eps_0 + chi_y * z + chi_z * y
    # For uniaxial bending (about y-axis): chi_z = 0
    # So: eps(z) = eps_0 + chi_y * z

    # Bottom fiber: eps(zmin) = eps_ctm
    # This gives: eps_ctm = eps_0 + chi_y * zmin

    # We need to find eps_0 and chi_y such that:
    # 1. eps(zmin) = eps_ctm (bottom fiber at cracking)
    # 2. Internal axial force equals external force n

    # From condition 1: eps_0 = eps_ctm - chi_y * zmin

    # Use bisection to find curvature that gives equilibrium
    # while keeping bottom fiber at cracking strain

    calculator = section.section_calculator

    # Get integration data if it exists, otherwise None
    integration_data = getattr(calculator, 'integration_data', None)
    mesh_size = getattr(calculator, 'mesh_size', 0.01)

    # Define a reasonable range for curvature
    # Start with very small curvature
    chi_min = -1e-3
    chi_max = 1e-3

    ITMAX = 100
    tolerance = 1e-2  # Force tolerance in N

    try:
        # Evaluate at bounds
        eps_0_a = eps_ctm - chi_min * zmin
        N_a, _, _, integration_data = calculator.integrator.integrate_strain_response_on_geometry(
            section.geometry,
            [eps_0_a, chi_min, 0.0],
            integration_data=integration_data,
            mesh_size=mesh_size
        )
        dn_a = N_a - n

        eps_0_b = eps_ctm - chi_max * zmin
        N_b, _, _, _ = calculator.integrator.integrate_strain_response_on_geometry(
            section.geometry,
            [eps_0_b, chi_max, 0.0],
            integration_data=integration_data,
            mesh_size=mesh_size
        )
        dn_b = N_b - n

        # Check if solution is within range of chi_min and chi_max
        if dn_a * dn_b > 0:
            # Expand the search range
            print("Warning: Initial range doesn't bracket solution, expanding search...")
            if abs(dn_a) < abs(dn_b):
                chi_max = chi_min
                chi_min = chi_min - 0.01
            else:
                chi_min = chi_max
                chi_max = chi_max + 0.01

            eps_0_a = eps_ctm - chi_min * zmin
            N_a, _, _, _ = calculator.integrator.integrate_strain_response_on_geometry(
                section.geometry,
                [eps_0_a, chi_min, 0.0],
                integration_data=integration_data,
                mesh_size=mesh_size
            )
            dn_a = N_a - n

        # Bisection algorithm
        it = 0
        while abs(dn_a - dn_b) > tolerance and it < ITMAX:
            chi_c = (chi_min + chi_max) / 2.0
            eps_0_c = eps_ctm - chi_c * zmin

            N_c, _, _, _ = calculator.integrator.integrate_strain_response_on_geometry(
                section.geometry,
                [eps_0_c, chi_c, 0.0],
                integration_data=integration_data,
                mesh_size=mesh_size
            )
            dn_c = N_c - n

            if dn_c * dn_a < 0:
                chi_max = chi_c
                dn_b = dn_c
            else:
                chi_min = chi_c
                dn_a = dn_c

            it += 1

        if it >= ITMAX:
            print(f"Warning: Maximum iterations reached. Force imbalance: {dn_c:.2f} N")

        # Use final values
        chi_y_eq = chi_c
        eps_0_eq = eps_0_c
        strain_profile = [eps_0_eq, chi_y_eq, 0.0]

        # Strain at bottom and top fibers
        eps_top = get_strain_at_point(strain_profile, 0, zmax)
        eps_bot = get_strain_at_point(strain_profile, 0, zmin)

        # print(f"\nStrain profile at cracking:")
        # print(f"  eps_0   = {eps_0_eq:.6e}")
        # print(f"  chi_y   = {chi_y_eq:.6e} mm⁻¹")
        # print(f"  eps_top = {eps_top:.6e} ")
        # print(f"  eps_bot = {eps_bot:.6e} ")
        #
        # print(
        #     f"\n{'Reinf':>6} "
        #     f"{'z [mm]':>9} "
        #     f"{'eps_ini [‰]':>14} "
        #     f"{'eps_bending [‰]':>16} "
        #     f"{'eps_total [‰]':>16}"
        # )
        # print("-" * 65)

        # --- Calculate Reinforcement Strains ---
        reinforcement_strains = []
        for i, z_s in enumerate(z_reinforcements):
            # Total strain = initial strain + bending strain
            eps_bending = eps_0_eq + chi_y_eq * z_s
            eps_total = eps_ini_list[i] + eps_bending
            reinforcement_strains.append(eps_total)

            # print(
            #     f"{i + 1:>6d} "
            #     f"{z_s:>9.2f} "
            #     f"{eps_ini_list[i]*1000:>+14.6f} "
            #     f"{eps_bending*1000:>+16.6f} "
            #     f"{eps_total*1000:>+16.6f}"
            # )
        # --- Calculate Internal Forces ---
        N_cr, My_cr, Mz_cr = section.section_calculator.integrate_strain_profile(
            strain=strain_profile,
            integrate='stress'
        )

        # print(f"\nInternal forces at cracking:")
        # print(f"  N = {N_cr:.2f} N (target: {n:.2f} N)")
        # print(f"  My = {My_cr:.2f} Nmm")
        # print(f"  Mz = {Mz_cr:.2f} Nmm")
        # print(f"\nCracking moment M_cr = {My_cr / 1e6:.2f} kNm")

        # Return results_c1_1
        return {
            'm_cr': My_cr,
            'strain_profile': strain_profile,
            'reinforcement_strains': reinforcement_strains,
            'stress_resultants': [N_cr, My_cr, Mz_cr],
            'eps_0': eps_0_eq,
            'chi_y': chi_y_eq,
            'eps_ctm': eps_ctm
        }

    except Exception as e:
        print(f"Error in equilibrium calculation: {e}")
        raise


# Helper function to calculate strain at any point
def get_strain_at_point(strain_profile, y, z):
    """
    Author: Elliot Melcer
    Calculate strain at point (y, z) given strain profile.

    Args:
        strain_profile: [eps_0, chi_y, chi_z]
        y: y-coordinate
        z: z-coordinate

    Returns:
        float: Strain at point (y, z)
    """
    eps_0, chi_y, chi_z = strain_profile
    return eps_0 + chi_y * z + chi_z * y

def sls_section(section_uls: GenericSection) -> GenericSection:
    """
    Author: Elliot Melcer
    Returns the section with sls constitutive law for concrete
    """
    # get the geometry of the section
    geo = section_uls.geometry

    #create sls concrete from concrete used in section
    concrete_sls = create_concrete(fck=get_concrete(section_uls).fck, constitutive_law='sargin', name = f"C{get_concrete(section_uls).fck} SLS")

    processed_geoms = []
    for g in geo.geometries:
        processed_geoms.append(
            SurfaceGeometry.from_geometry(geo=g, new_material=concrete_sls) # change concrete material
        )
    for pg in geo.point_geometries:
        processed_geoms.append(pg) # keep same reinforcement material

    new_sls_section = GenericSection(CompoundGeometry(geometries=processed_geoms))

    return new_sls_section

def get_concrete(section: GenericSection) -> Concrete:
    """
    Author: Elliot Melcer
    Return the first concrete material found in the section geometry.
    Raises:
        ValueError: If no concrete material exists in the geometry.
    """
    # For CompoundGeometry, get material from the first surface geometry
    geometry = section.geometry
    if hasattr(geometry, 'geometries'):
        # CompoundGeometry - get concrete from first surface
        concrete = geometry.geometries[0].material
    else:
        # Simple SurfaceGeometry
        concrete = geometry.material

    return concrete

def get_reinforcement(section: GenericSection) -> tuple[Reinforcement, float]:
    """
    Author: Elliot Melcer
    Returns the first Reinforcement material found in the section geometry and the corresponding Reinforcement area
    (assumption: all Reinforcement diameters are the same).

    Raises:
        ValueError: If no reinforcement material is found.
    """

    geometry = section.geometry

    # simple surface / not compound? then nothing to check
    if not hasattr(geometry, "geometries"):
        raise ValueError("Geometry does not contain reinforcement points.")

    # compound → scan point geometries
    if hasattr(geometry, "point_geometries"):
        for geo in geometry.point_geometries:
            mat = getattr(geo, "material", None)
            area = (geo.diameter ** 2 / 4) * np.pi
            if isinstance(mat, Reinforcement):
                return mat, area

    raise ValueError("No reinforcement material found in section geometry.")

def get_number_of_reinforcements(section: GenericSection) -> int:
    """
    Author: Elliot Melcer
    Count the number of reinforcement point geometries in the section geometry.
    """
    geom = section.geometry
    n = len(geom.point_geometries)
    return n
