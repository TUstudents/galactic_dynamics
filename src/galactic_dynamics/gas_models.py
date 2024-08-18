import numpy as np
from .constants import k_B, m_p

def gas_density(r, r_g, M_g):
    """
    Calculate the gas density profile.
    
    Args:
        r (float or array): Radial distance(s) in meters.
        r_g (float): Gas scale radius in meters.
        M_g (float): Total gas mass in kg.
    
    Returns:
        float or array: Gas density in kg/m^3.
    """
    return M_g / (2 * np.pi * r_g**2) * np.exp(-r / r_g)

def pressure_gradient(r, r_g, M_g, T):
    """
    Calculate the pressure gradient of the gas.
    
    Args:
        r (float or array): Radial distance(s) in meters.
        r_g (float): Gas scale radius in meters.
        M_g (float): Total gas mass in kg.
        T (float): Gas temperature in Kelvin.
    
    Returns:
        float or array: Pressure gradient in Pa/m.
    """
    r = np.atleast_1d(r)
    rho = gas_density(r, r_g, M_g)
    
    if len(r) == 1:
        # For a single point, use the analytical derivative
        drho_dr = -rho / r_g
    else:
        # For multiple points, use np.gradient
        drho_dr = np.gradient(rho, r)
    
    return -k_B * T / (m_p * r) * drho_dr

def turbulence_pressure(r, r_g, M_g, v_turb):
    """
    Calculate the turbulence pressure.
    
    Args:
        r (float or array): Radial distance(s) in meters.
        r_g (float): Gas scale radius in meters.
        M_g (float): Total gas mass in kg.
        v_turb (float): Turbulent velocity in m/s.
    
    Returns:
        float or array: Turbulence pressure in Pa.
    """
    rho = gas_density(r, r_g, M_g)
    return rho * v_turb**2