# Galactic Dynamics

A Python package for modeling galactic dynamics including advanced effects such as gas dynamics, magnetic fields, and cosmic rays.

## Installation

For development use pip install -e .

```bash
pip install galactic-dynamics
```

## Quick Start

```python
import numpy as np
from galactic_dynamics import solve_velocity
from galactic_dynamics.constants import pc, M_sun

# Define galaxy parameters
galaxy_params = (3e3*pc, 5e10*M_sun, 500*pc, 1e10*M_sun, 20e3*pc, 1e12*M_sun)
gas_params = (4e3*pc, 1e10*M_sun, 1e4, 1e4, 1e-10, 5e3*pc, 0.1, 1e-12, 10e3*pc, -1e3)

# Generate radial points
r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 1000)

# Solve for velocity
v = solve_velocity(r, galaxy_params, gas_params)

# Plot the results
import matplotlib.pyplot as plt
plt.plot(r/pc, v/1000)
plt.xlabel('Radius (pc)')
plt.ylabel('Velocity (km/s)')
plt.xscale('log')
plt.show()
```

## Features

- Mass models for disk, bulge, and halo components
- Gas dynamics including pressure and turbulence
- Magnetic field effects
- Cosmic ray pressure
- Advanced velocity solver incorporating all effects

## Documentation

For full documentation, please visit [our documentation site](https://galactic-dynamics.readthedocs.io).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0). To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file in the repository.