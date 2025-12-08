import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from structuralcodes.core._section_results import MomentCurvatureResults
from structuralcodes.geometry import Geometry
from structuralcodes.materials.concrete import Concrete
from structuralcodes.materials.reinforcement import Reinforcement
from structuralcodes.sections import GenericSection
from tabulate import tabulate

# --- Moment-Curvature-Diagram ---

def plot_moment_curvature(m_c_res: MomentCurvatureResults, x = None, ax=None):
    """
            Author: Elliot Melcer
            Plot moment–curvature (M–K) diagram with My and Mu annotations.
            """

    import matplotlib.pyplot as plt

    # Create figure/axes if not provided
    if ax is None:
        fig, ax = plt.subplots()

        # ============================================================
        #              Plot continuous M–K curve
        # ============================================================
    ax.plot(-m_c_res.chi_y * 1e6, -m_c_res.m_y / 1e6,
            color="black", linewidth=1.5, label="M–K curve")

    # ============================================================
    #              Plot ALL points as small purple dots
    # ============================================================
    ax.scatter(-m_c_res.chi_y * 1e6, -m_c_res.m_y / 1e6,
               s=6, color="purple", label="M–K points")

    # ============================================================
    #                    ULTIMATE POINT (Mu)
    # ============================================================
    x_u = -m_c_res.chi_y[-1] * 1e6
    y_u = -m_c_res.m_y[-1] / 1e6

    # Dot
    ax.plot(x_u, y_u, 'ro', markersize=5)

    # Label
    label_u = (
        f"(K_u = {m_c_res.chi_y[-1] * 1e6 :.3e},\n"
        f" M_u = {m_c_res.m_y[-1] / 1e6:.3f} kNm)"
    )
    ax.text(
        x_u, y_u, label_u,
        fontsize=10, color="red",
        ha="right", va="bottom"
    )

    # ============================================================
    #                    YIELDING POINT (My)
    # ============================================================
    idx_y = 20 - 1  # 20th point (Python index 19)

    x_y = -m_c_res.chi_y[idx_y] * 1e6
    y_y = -m_c_res.m_y[idx_y] / 1e6

    # Dot
    ax.plot(x_y, y_y, 'ro', markersize=5)

    # Label
    label_y = (
        f"(K_y = {m_c_res.chi_y[idx_y] * 1e6 :.3e},\n"
        f" M_y = {m_c_res.m_y[idx_y] / 1e6:.3f} kNm)"
    )
    ax.text(
        x_y, y_y, label_y,
        fontsize=10, color="red",
        ha="right", va="top"
    )

    # --- Axis labels ---
    ax.set_xlabel("K [1/1000m]")
    ax.set_ylabel("My [kNm]")

    # --- Grid ---
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # ---- Add title here ----
    ax.set_title(f"M-K-Diagram at x = {x} * L")

    return ax

def table_moment_curvature(m_c_res: MomentCurvatureResults):
        """
        Author: Elliot Melcer
        Return a tabulated string of moment–curvature results.
        """
        # Convert to numpy arrays for safety
        chi_y = np.asarray(m_c_res.chi_y)
        chi_z = np.asarray(m_c_res.chi_z) if m_c_res.chi_z is not None else None
        eps_axial = np.asarray(m_c_res.eps_axial)
        m_y = np.asarray(m_c_res.m_y)
        m_z = np.asarray(m_c_res.m_z) if m_c_res.m_z is not None else None

        # Build table rows
        rows = []
        for i in range(len(chi_y)):
            rows.append([
                i,
                chi_y[i],
                chi_z[i] if chi_z is not None else None,
                eps_axial[i],
                m_y[i],
                m_z[i] if m_z is not None else None,
            ])

        headers = ["i", "chi_y", "chi_z", "eps_axial", "m_y", "m_z"]

        return tabulate(rows, headers=headers, floatfmt=".3e", tablefmt="fancy_grid")

# --- Concrete ---

def plot_constitutive_law_concrete(concrete: Concrete, n: int = 100):
    """
    Author: Elliot Melcer
    Plot the constitutive law (stress–strain curve) for this concrete material
    """

    if concrete.constitutive_law is None:
        raise ValueError("No constitutive law is attached to this Concrete instance.")

    law = concrete.constitutive_law

    # Build strain range based on law parameters if present
    eps_min, _ = law.get_ultimate_strain()
    eps_0 = getattr(law, "_eps_0", -0.002)

    eps = np.linspace(eps_min, 0.0, n)
    sig = law.get_stress(eps)

    # === FLIP OVER X AND Y AXIS ===
    eps_plot = -eps
    sig_plot = -sig

    fig, ax = plt.subplots()
    ax.plot(eps_plot, sig_plot, linewidth=1.8, color="black", label=law.name)

    ax.set_xlabel("Strain [-]")
    ax.set_ylabel("Stress [MPa]")
    ax.set_title(f"Constitutive Law of {concrete.name}")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    # plt.show()

# --- Reinforcement ---

def plot_constitutive_law_reinforcement(reinforcement: Reinforcement, n: int = 100):
    """
            Author: Elliot Melcer
            Plot the reinforcement stress–strain constitutive law.

            No flipping of axes is performed. Positive strain → positive stress.
            """

    import numpy as np
    import matplotlib.pyplot as plt

    # Check constitutive law
    if reinforcement.constitutive_law is None:
        raise ValueError(
            "No constitutive law is attached to this Reinforcement instance."
        )

    law = reinforcement.constitutive_law

    # ------------------------------------------------------------
    #   Build strain domain for steel
    # ------------------------------------------------------------
    eps_y = reinforcement.epsyk  # yield strain
    eps_u = reinforcement.epsud()  # ultimate strain

    # Positive strain range typical for reinforcement
    eps = np.linspace(0.0, eps_u * 1.0, n)

    # Compute stresses (in MPa)
    sig = law.get_stress(eps)

    # ------------------------------------------------------------
    #   Plot
    # ------------------------------------------------------------
    fig, ax = plt.subplots()
    ax.plot(
        eps, sig,
        color="black", linewidth=1.8,
        label=f"{reinforcement.name} ({law.name})"
    )

    # ---------------------------------------------
    #   Axes & grid
    # ---------------------------------------------
    ax.set_xlabel("Strain [-]")
    ax.set_ylabel("Stress [MPa]")
    ax.set_title("Reinforcement Constitutive Law")
    ax.grid(True, linestyle="--", alpha=0.55)
    ax.legend()

    # plt.show()

# --- Cross Section ---

def plot_cross_section(gs: GenericSection, ax=None, x=None, **kwargs):
    """
    Author: Elliot Melcer
    Plot the section geometry, its centroid, and the local coordinate system.

    Parameters
    ----------
     ax : matplotlib.axes.Axes, optional
         Axis to draw on. If None, a new figure is created.
     x : float, optional longitudinal coordinate for title.
     kwargs : dict
         Extra args passed to geometry.plot().
     gs: GenericSection
         Generic section geometry.
    """

    # Create axes if needed
    if ax is None:
        fig, ax = plt.subplots()

    # ---- 1. Plot the geometry using geometry method ----
    _plot_geometry(gs.geometry, ax=ax, x=x, **kwargs)

    # ---- 2. Plot the section centroid ----
    cy = gs.gross_properties.cy
    cz = gs.gross_properties.cz

    ax.scatter(cy, cz, color="red", s=10, zorder=10)
    ax.text(cy, cz, f" C({cy:.2f}, {cz:.2f})",
            color="red", va="bottom", ha="left")

    # ---- 3. Plot local coordinate system at (0,0) ----
    x_min, x_max, y_min, y_max = gs.geometry.calculate_extents()
    L = 0.1 * (y_max-y_min)

    # y-axis → positive x direction
    ax.arrow(0, 0, L, 0,
             head_width=L * 0.3, head_length=L * 0.3,
             fc="black", ec="black", alpha = 0.4)
    ax.text(L * 1.5, 0, "y", va="center", ha="left", color="black", alpha = 0.4)

    # z-axis → positive y direction
    ax.arrow(0, 0, 0, L,
             head_width=L * 0.3, head_length=L * 0.3,
             fc="black", ec="black", alpha = 0.4)
    ax.text(0, L * 1.5, "z", va="bottom", ha="center", color="black", alpha = 0.4)

    # ---- 4. Final formatting ----
    ax.set_title(f"Section at x = {x} * L" if x is not None else "Section")
    ax.set_aspect("equal")

    return ax

# --- Geometry ---

def _plot_geometry(geo: Geometry, ax=None, x = None, **kwargs):
    """
    Author: Elliot Melcer
    Plot any Geometry, SurfaceGeometry, PointGeometry, or CompoundGeometry object.

    Parameters
    ----------
    geo : Geometry
        The geometry object to plot.
    ax : matplotlib.axes.Axes, optional
        Existing axis to draw on. If None, a new figure is created.
    kwargs : dict
        Extra keyword arguments for styling (e.g. color="blue", linewidth=2).
    """

    if ax is None:
        fig, ax = plt.subplots()

    # Surface geometry
    if hasattr(geo, "polygon"):
        poly = geo.polygon
        _plot_polygon(poly, ax, **kwargs, edgecolor="grey", facecolor="lightgrey")

    # Point geometry
    if hasattr(geo, "point"):
        circ = geo.point.buffer(geo.diameter / 2)
        _plot_polygon(circ, ax, **kwargs, edgecolor="black", facecolor="black")

    # Compound geometry
    if hasattr(geo, "geometries"):
        for g in geo.geometries:
            _plot_geometry(g, ax=ax, show=False, **kwargs)
        for p in geo.point_geometries:
            _plot_geometry(p, ax=ax, show=False, **kwargs)

    ax.set_aspect("equal")

    # ---- Add title here ----
    ax.set_title(f"Cross-Section at x = {x} * L")

    # remove frame
    for spine in ax.spines.values():
        spine.set_visible(False)

    # if show:
    #     plt.show()
    return ax

def _plot_polygon(poly: Polygon, ax, edgecolor="black", facecolor="lightgrey", **kwargs):
    """
    Author: Elliot Melcer
    Plot and fill a Shapely polygon (supports holes).
    """
    # --- Fill exterior ---
    x, y = poly.exterior.xy
    ax.fill(x, y, facecolor=facecolor, edgecolor=edgecolor)

    # --- Fill holes (white) ---
    for hole in poly.interiors:
        hx, hy = hole.xy
        ax.fill(hx, hy, facecolor="white", edgecolor=edgecolor, linestyle="--")
