import numpy as np
import pytest
from galactic_dynamics.cosmic_ray_models import cosmic_ray_pressure, cosmic_ray_gradient
from galactic_dynamics.constants import pc

@pytest.fixture
def cosmic_ray_params():
    return (1e-12, 10e3*pc)

def test_cosmic_ray_pressure(cosmic_ray_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    P_cr0, r_cr = cosmic_ray_params
    pressure = cosmic_ray_pressure(r, P_cr0, r_cr)
    assert np.all(pressure > 0), "Cosmic ray pressure should be positive"
    assert pressure[0] > pressure[-1], "Cosmic ray pressure should decrease with radius"

def test_cosmic_ray_gradient(cosmic_ray_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    grad = cosmic_ray_gradient(r, *cosmic_ray_params)
    assert np.all(grad < 0), "Cosmic ray pressure gradient should be negative"