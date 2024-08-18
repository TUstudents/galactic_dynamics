import numpy as np
import matplotlib.pyplot as plt
from galactic_dynamics import solve_velocity, enclosed_mass
from galactic_dynamics.constants import G, pc

def plot_rotation_curve(galaxy_params, gas_params):
    # Radial distances
    R = np.logspace(np.log10(100*pc), np.log10(100*1000*pc), 1000)  # 100 pc to 100 kpc

    # Calculate velocities
    v_odeint = solve_velocity(R, galaxy_params, gas_params, method='odeint')
    v_rk4 = solve_velocity(R, galaxy_params, gas_params, method='rk4')
    v_n = np.sqrt(G * enclosed_mass(R, galaxy_params) / R)

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.plot(R/1000/pc, v_n/1000, label='Newtonian', linestyle='--')
    plt.plot(R/1000/pc, v_odeint/1000, label='ODEINT')
    plt.plot(R/1000/pc, v_rk4/1000, label='RK4')
    plt.xlabel('Radius (kpc)')
    plt.ylabel('Rotation Velocity (km/s)')
    plt.title('Galaxy Rotation Curve: Comparison of Numerical Methods')
    plt.legend()
    plt.xscale('log')
    plt.ylim(0, 300)
    plt.grid(True)
    plt.show()

    # Calculate and print the average differences
    avg_diff_odeint = np.mean((v_odeint - v_n) / v_n) * 100
    avg_diff_rk4 = np.mean((v_rk4 - v_n) / v_n) * 100
    print(f"ODEINT: Average difference from Newtonian model: {avg_diff_odeint:.2f}%")
    print(f"RK4: Average difference from Newtonian model: {avg_diff_rk4:.2f}%")
    print(f"Difference between ODEINT and RK4: {np.mean(np.abs(v_odeint - v_rk4))/1000:.4f} km/s")

if __name__ == "__main__":
    # Galaxy parameters (r_d, M_d, r_b, M_b, r_h, M_h) in SI units
    galaxy_params = (3e3*pc, 5e10*1.989e30, 500*pc, 1e10*1.989e30, 20e3*pc, 1e12*1.989e30)

    # Gas parameters (r_g, M_g, T, v_turb, B0, r_B, reconnection_rate, P_cr0, r_cr, v_flow)
    gas_params = (4e3*pc, 1e10*1.989e30, 1e4, 1e4, 1e-10, 5e3*pc, 0.1, 1e-12, 10e3*pc, -1e3)

    plot_rotation_curve(galaxy_params, gas_params)