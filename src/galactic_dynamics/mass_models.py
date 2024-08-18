import numpy as np
from scipy.integrate import simps
from .constants import G, M_sun, pc

def mass_density(r, params):
    """
    Calculate the mass density profile of the galaxy.
    
    Args:
        r (array): Radial distances in meters.
        params (tuple): (r_d, M_d, r_b, M_b, r_h, M_h) in SI units.
    
    Returns:
        array: Mass density in kg/m^3.
    """
    r_d, M_d, r_b, M_b, r_h, M_h = params
    disk = M_d / (2 * np.pi * r_d**2) * np.exp(-r / r_d)
    bulge = M_b / (2 * np.pi * r_b**3) * np.exp(-r / r_b)
    halo = M_h / (4 * np.pi * r_h**3) * (1 + r/r_h)**-2
    return disk + bulge + halo

def enclosed_mass(r, params):
    """
    Calculate the enclosed mass up to radius r.
    
    Args:
        r (float or array): Radial distance(s) in meters.
        params (tuple): Galaxy parameters.
    
    Returns:
        array: Enclosed mass in kg.
    """
    r = np.atleast_1d(r)
    r_min = r.min() / 10
    r_max = r.max() * 10
    r_array = np.geomspace(r_min, r_max, 10000)
    density = mass_density(r_array, params)
    integrand = density * 4 * np.pi * r_array**2
    mass = np.array([simps(integrand[r_array <= ri], r_array[r_array <= ri]) for ri in r])
    return mass

def analytical_mass(r, params):
    """
    Calculate the analytical enclosed mass for simple profiles.
    
    Args:
        r (float or array): Radial distance(s) in meters.
        params (tuple): Galaxy parameters.
    
    Returns:
        array: Enclosed mass in kg.
    """
    r = np.atleast_1d(r)
    r_d, M_d, r_b, M_b, r_h, M_h = params
    
    # Disk (approximation for thin disk)
    disk_mass = M_d * (1 - (1 + r/r_d) * np.exp(-r/r_d))
    
    # Bulge (assuming it follows a Hernquist profile)
    bulge_mass = M_b * r**2 / (r + r_b)**2
    
    # Halo (NFW profile)
    halo_mass = M_h * (np.log(1 + r/r_h) - (r/r_h) / (1 + r/r_h))
    
    return disk_mass + bulge_mass + halo_mass