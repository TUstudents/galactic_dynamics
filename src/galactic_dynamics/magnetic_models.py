import numpy as np

def magnetic_field_strength(r, B0, r_B):
    """
    Calculate the magnetic field strength profile.
    
    Args:
        r (array): Radial distances in meters.
        B0 (float): Central magnetic field strength in Tesla.
        r_B (float): Magnetic field scale radius in meters.
    
    Returns:
        array: Magnetic field strength in Tesla.
    """
    return B0 * np.exp(-r / r_B)

def magnetic_pressure(B):
    """
    Calculate the magnetic pressure.
    
    Args:
        B (array): Magnetic field strength in Tesla.
    
    Returns:
        array: Magnetic pressure in Pa.
    """
    return B**2 / (2 * np.pi * 4e-7)  # Using mu0 = 4π × 10^-7 N/A^2

def magnetic_reconnection_heating(r, B, reconnection_rate):
    """
    Calculate heating due to magnetic reconnection.
    
    Args:
        r (array): Radial distances in meters.
        B (array): Magnetic field strength in Tesla.
        reconnection_rate (float): Reconnection rate (dimensionless).
    
    Returns:
        array: Heating rate in W/m^3.
    """
    return reconnection_rate * B**2 / (8 * np.pi * 4e-7)  # Using mu0 = 4π × 10^-7 N/A^2