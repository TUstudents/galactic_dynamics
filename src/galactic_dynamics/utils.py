import numpy as np

def kpc_to_m(distance_kpc):
    """Convert distance from kpc to meters."""
    return distance_kpc * 3.085677581e19

def m_to_kpc(distance_m):
    """Convert distance from meters to kpc."""
    return distance_m / 3.085677581e19

def km_s_to_m_s(velocity_km_s):
    """Convert velocity from km/s to m/s."""
    return velocity_km_s * 1000

def m_s_to_km_s(velocity_m_s):
    """Convert velocity from m/s to km/s."""
    return velocity_m_s / 1000

def calculate_circular_velocity(mass, radius):
    """Calculate circular velocity for a given mass and radius."""
    G = 6.67430e-11  # gravitational constant
    return np.sqrt(G * mass / radius)