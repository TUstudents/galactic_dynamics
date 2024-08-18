import numpy as np
import pytest
from galactic_dynamics.mass_models import mass_density, enclosed_mass, analytical_mass
from galactic_dynamics.constants import pc, M_sun

@pytest.fixture
def galaxy_params():
    return (3e3*pc, 5e10*M_sun, 500*pc, 1e10*M_sun, 20e3*pc, 1e12*M_sun)

def test_mass_density(galaxy_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    density = mass_density(r, galaxy_params)
    assert np.all(density > 0), "Density should be positive"
    assert density[0] > density[-1], "Density should decrease with radius"

def test_enclosed_mass(galaxy_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    mass_numerical = enclosed_mass(r, galaxy_params)
    mass_analytical = analytical_mass(r, galaxy_params)
    
    assert np.all(np.diff(mass_numerical) >= 0), "Enclosed mass should be monotonically increasing"
    
    total_mass = sum(galaxy_params[1::2])
    assert np.isclose(mass_numerical[-1], total_mass, rtol=0.1), f"Total numerical mass should match input. Expected {total_mass}, got {mass_numerical[-1]}"
    assert np.isclose(mass_analytical[-1], total_mass, rtol=0.1), f"Total analytical mass should match input. Expected {total_mass}, got {mass_analytical[-1]}"
    
    # Compare numerical and analytical solutions
    assert np.allclose(mass_numerical, mass_analytical, rtol=0.1), "Numerical and analytical solutions should be close"

def test_mass_conservation(galaxy_params):
    r_inner = 1*pc
    r_outer = 1e6*pc  # Very large radius
    mass_inner = enclosed_mass(np.array([r_inner]), galaxy_params)[0]
    mass_outer = enclosed_mass(np.array([r_outer]), galaxy_params)[0]
    total_mass = sum(galaxy_params[1::2])
    
    assert mass_inner < 0.01 * total_mass, f"Mass at {r_inner/pc} pc should be small. Got {mass_inner/M_sun} M_sun"
    assert np.isclose(mass_outer, total_mass, rtol=0.01), f"Mass at large radius should match total. Expected {total_mass/M_sun} M_sun, got {mass_outer/M_sun} M_sun"

def test_specific_radii(galaxy_params):
    M_d, M_b, M_h = galaxy_params[1::2]
    r_d, r_b, r_h = galaxy_params[::2]
    
    # At r_d, should have ~63% of disk mass
    mass_at_rd = enclosed_mass(np.array([r_d]), galaxy_params)[0]
    expected_mass_at_rd = 0.63 * M_d + analytical_mass(np.array([r_d]), galaxy_params)[0] - 0.63 * M_d
    assert np.isclose(mass_at_rd, expected_mass_at_rd, rtol=0.1), f"Mass at r_d incorrect. Expected {expected_mass_at_rd}, got {mass_at_rd}"
    
    # At 10*r_h, should have almost all mass
    total_mass = sum(galaxy_params[1::2])
    mass_at_10rh = enclosed_mass(np.array([10*r_h]), galaxy_params)[0]
    assert np.isclose(mass_at_10rh, total_mass, rtol=0.01), f"Mass at 10*r_h should be close to total mass. Expected {total_mass}, got {mass_at_10rh}"