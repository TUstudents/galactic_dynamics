import numpy as np
import pytest
from galactic_dynamics.magnetic_models import magnetic_field_strength, magnetic_pressure, magnetic_reconnection_heating
from galactic_dynamics.constants import pc

@pytest.fixture
def magnetic_params():
    return (1e-10, 5e3*pc, 0.1)

def test_magnetic_field_strength(magnetic_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    B0, r_B, _ = magnetic_params
    B = magnetic_field_strength(r, B0, r_B)
    assert np.all(B > 0), "Magnetic field strength should be positive"
    assert B[0] > B[-1], "Magnetic field strength should decrease with radius"

def test_magnetic_pressure(magnetic_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    B0, r_B, _ = magnetic_params
    B = magnetic_field_strength(r, B0, r_B)
    pressure = magnetic_pressure(B)
    assert np.all(pressure > 0), "Magnetic pressure should be positive"
    assert pressure[0] > pressure[-1], "Magnetic pressure should decrease with radius"

def test_magnetic_reconnection_heating(magnetic_params):
    r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 100)
    B0, r_B, reconnection_rate = magnetic_params
    B = magnetic_field_strength(r, B0, r_B)
    heating = magnetic_reconnection_heating(r, B, reconnection_rate)
    assert np.all(heating > 0), "Magnetic reconnection heating should be positive"
    assert heating[0] > heating[-1], "Magnetic reconnection heating should decrease with radius"