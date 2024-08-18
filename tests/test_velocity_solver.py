import numpy as np
import pytest
from galactic_dynamics.velocity_solver import solve_velocity, solve_velocity_odeint, solve_velocity_rk4
from galactic_dynamics.constants import pc, M_sun, G

@pytest.fixture
def galaxy_params():
    return (3e3*pc, 5e10*M_sun, 500*pc, 1e10*M_sun, 20e3*pc, 1e12*M_sun)

@pytest.fixture
def gas_params():
    return (4e3*pc, 1e10*M_sun, 1e4, 1e4, 1e-10, 5e3*pc, 0.1, 1e-12, 10e3*pc, -1e3)

@pytest.fixture
def radial_points():
    return np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)

def test_solve_velocity_odeint(galaxy_params, gas_params, radial_points):
    v = solve_velocity_odeint(radial_points, galaxy_params, gas_params)
    assert np.all(v > 0), "Velocities should be positive"
    assert np.all(np.diff(v[:len(v)//2]) > 0), "Velocity should increase in inner region"
    assert np.allclose(np.diff(v[len(v)//2:]), 0, atol=1e3), "Velocity should be approximately flat in outer region"

def test_solve_velocity_rk4(galaxy_params, gas_params, radial_points):
    v = solve_velocity_rk4(radial_points, galaxy_params, gas_params)
    assert np.all(v > 0), "Velocities should be positive"
    assert np.all(np.diff(v[:len(v)//2]) > 0), "Velocity should increase in inner region"
    assert np.allclose(np.diff(v[len(v)//2:]), 0, atol=1e3), "Velocity should be approximately flat in outer region"

def test_solve_velocity_methods_consistency(galaxy_params, gas_params, radial_points):
    v_odeint = solve_velocity(radial_points, galaxy_params, gas_params, method='odeint')
    v_rk4 = solve_velocity(radial_points, galaxy_params, gas_params, method='rk4')
    assert np.allclose(v_odeint, v_rk4, rtol=1e-3, atol=1e3), "ODEINT and RK4 methods should produce similar results"

def test_solve_velocity_invalid_method(galaxy_params, gas_params, radial_points):
    with pytest.raises(ValueError):
        solve_velocity(radial_points, galaxy_params, gas_params, method='invalid')

def test_solve_velocity_keplerian_limit(galaxy_params, gas_params):
    r = np.array([1e20, 1e21])  # Test at large radii
    v = solve_velocity(r, galaxy_params, gas_params, method='rk4')
    M_total = sum(galaxy_params[1::2])  # Sum of all mass components
    v_keplerian = np.sqrt(G * M_total / r)
    assert np.allclose(v, v_keplerian, rtol=0.1), "Velocity should approach Keplerian limit at large radii"