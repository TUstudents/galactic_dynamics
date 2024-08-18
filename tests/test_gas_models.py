import numpy as np
import pytest
from galactic_dynamics.gas_models import gas_density, pressure_gradient, turbulence_pressure
from galactic_dynamics.constants import pc, M_sun

@pytest.fixture
def gas_params():
    return (4e3*pc, 1e10*M_sun, 1e4, 1e4)

def test_gas_density(gas_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    r_g, M_g, _, _ = gas_params
    density = gas_density(r, r_g, M_g)
    assert np.all(density > 0), "Gas density should be positive"
    assert density[0] > density[-1], "Gas density should decrease with radius"

def test_pressure_gradient(gas_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    r_g, M_g, T, _ = gas_params
    grad = pressure_gradient(r, r_g, M_g, T)
    assert np.all(grad <= 0), "Pressure gradient should be negative or zero"

def test_turbulence_pressure(gas_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    r_g, M_g, _, v_turb = gas_params
    pressure = turbulence_pressure(r, r_g, M_g, v_turb)
    assert np.all(pressure > 0), "Turbulence pressure should be positive"
    assert pressure[0] > pressure[-1], "Turbulence pressure should decrease with radius"