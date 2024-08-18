Tutorial
========

Getting Started
---------------

To use the Galactic Dynamics package, first install it using pip:

.. code-block:: bash

   pip install galactic-dynamics

Basic Usage
-----------

Here's a simple example of how to generate a rotation curve:

.. code-block:: python

   import numpy as np
   from galactic_dynamics import solve_velocity
   from galactic_dynamics.constants import pc, M_sun

   # Define galaxy parameters
   galaxy_params = (3e3*pc, 5e10*M_sun, 500*pc, 1e10*M_sun, 20e3*pc, 1e12*M_sun)
   gas_params = (4e3*pc, 1e10*M_sun, 1e4, 1e4, 1e-10, 5e3*pc, 0.1, 1e-12, 10e3*pc, -1e3)

   # Generate radial points
   r = np.logspace(np.log10(100*pc), np.log10(100e3*pc), 1000)

   # Solve for velocity
   v = solve_velocity(r, galaxy_params, gas_params,method='rk4')

   # Plot the results
   import matplotlib.pyplot as plt
   plt.plot(r/pc, v/1000)
   plt.xlabel('Radius (pc)')
   plt.ylabel('Velocity (km/s)')
   plt.xscale('log')
   plt.show()

Advanced Usage
--------------

For more advanced usage, including customizing individual components of the model, 
refer to the API documentation.