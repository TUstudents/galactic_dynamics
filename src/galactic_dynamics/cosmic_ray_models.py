import numpy as np

def cosmic_ray_pressure(r, P_cr0, r_cr):
    """
    Calculate the cosmic ray pressure profile.
    
    Args:
        r (array): Radial distances in meters.
        P_cr0 (float): Central cosmic ray pressure in Pa.
        r_cr (float): Cosmic ray scale radius in meters.
    
    Returns:
        array: Cosmic ray pressure in Pa.
    """
    return P_cr0 * np.exp(-r / r_cr)

def cosmic_ray_gradient(r, P_cr0, r_cr):
    """
    Calculate the gradient of cosmic ray pressure.
    
    Args:
        r (array): Radial distances in meters.
        P_cr0 (float): Central cosmic ray pressure in Pa.
        r_cr (float): Cosmic ray scale radius in meters.
    
    Returns:
        array: Gradient of cosmic ray pressure in Pa/m.
    """
    P_cr = cosmic_ray_pressure(r, P_cr0, r_cr)
    return -P_cr / r_cr