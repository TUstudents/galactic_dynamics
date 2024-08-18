import numpy as np
from scipy.integrate import odeint
from .constants import G, c
from .mass_models import enclosed_mass
from .gas_models import gas_density, pressure_gradient, turbulence_pressure
from .magnetic_models import magnetic_field_strength, magnetic_pressure, magnetic_reconnection_heating
from .cosmic_ray_models import cosmic_ray_pressure, cosmic_ray_gradient

def total_acceleration(r, v, galaxy_params, gas_params):
    """Calculate total acceleration including all effects."""
    r_d, M_d, r_b, M_b, r_h, M_h = galaxy_params
    r_g, M_g, T, v_turb, B0, r_B, reconnection_rate, P_cr0, r_cr, v_flow = gas_params
    
    # Gravitational acceleration
    a_grav = -G * enclosed_mass(r, galaxy_params) / r**2
    
    # Gravitomagnetic effect
    omega = v / r
    a_gm = v**2 * omega * r / (2 * c**2)
    
    # Gas pressure
    rho_gas = gas_density(r, r_g, M_g)
    a_pressure = -pressure_gradient(r, r_g, M_g, T) / rho_gas
    
    # Turbulence
    if np.isscalar(r):
        a_turb = 0  # Assume no turbulence effect for single point
    else:
        a_turb = -np.gradient(turbulence_pressure(r, r_g, M_g, v_turb), r) / rho_gas
    
    # Magnetic effects
    B = magnetic_field_strength(r, B0, r_B)
    if np.isscalar(r):
        a_magnetic = 0  # Assume no magnetic effect for single point
    else:
        a_magnetic = -np.gradient(magnetic_pressure(B), r) / rho_gas
    
    # Cosmic ray pressure
    a_cr = cosmic_ray_gradient(r, P_cr0, r_cr) / rho_gas
    
    # Magnetic reconnection heating
    a_reconnection = magnetic_reconnection_heating(r, B, reconnection_rate) / (rho_gas * v)
    
    # Gas flow
    if np.isscalar(r):
        a_flow = 0  # Assume no flow effect for single point
    else:
        a_flow = v_flow * np.gradient(v_flow, r)
    
    return a_grav + a_gm + a_pressure + a_turb + a_magnetic + a_cr + a_reconnection + a_flow

def solve_velocity_odeint(r, galaxy_params, gas_params):
    """Solve for velocity profile using scipy's odeint."""
    def dv_dr(v, r):
        return total_acceleration(r, v, galaxy_params, gas_params)
    
    v_initial = np.sqrt(G * enclosed_mass(r[0], galaxy_params) / r[0])
    v = odeint(dv_dr, v_initial, r).flatten()
    return v

def rk4_step(r, v, h, galaxy_params, gas_params):
    """Perform a single step of the RK4 method."""
    k1 = total_acceleration(r, v, galaxy_params, gas_params)
    k2 = total_acceleration(r + 0.5*h, v + 0.5*h*k1, galaxy_params, gas_params)
    k3 = total_acceleration(r + 0.5*h, v + 0.5*h*k2, galaxy_params, gas_params)
    k4 = total_acceleration(r + h, v + h*k3, galaxy_params, gas_params)
    return v + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

def solve_velocity_rk4(r, galaxy_params, gas_params):
    """Solve for velocity profile using 4th-order Runge-Kutta method."""
    v = np.zeros_like(r)
    v[0] = np.sqrt(G * enclosed_mass(r[0], galaxy_params) / r[0])
    
    for i in range(1, len(r)):
        h = r[i] - r[i-1]
        v[i] = rk4_step(r[i-1], v[i-1], h, galaxy_params, gas_params)
    
    return v

def solve_velocity(r, galaxy_params, gas_params, method='rk4'):
    """Solve for velocity profile using specified method."""
    if method == 'odeint':
        return solve_velocity_odeint(r, galaxy_params, gas_params)
    elif method == 'rk4':
        return solve_velocity_rk4(r, galaxy_params, gas_params)
    else:
        raise ValueError("Invalid method. Choose 'odeint' or 'rk4'.")