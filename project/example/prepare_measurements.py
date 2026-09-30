"""
Preparation of synthetic measurements (measurements_friction.csv and measurements_fall.csv).

I do not have real measurements, so I generate them from the model and
add normally distributed noise. The generator seed is fixed so that the
data are reproducible.

* measurements_friction.csv: pulling force F at seven loads N
  (Coulomb friction with mu = 0.32, noise 4 N),
* measurements_fall.csv: angle of the ladder during a frictionless fall
  from 75 degrees, 30 frames per second, noise 0.5 degree, until
  detachment from the wall.
"""

import numpy as np
from scipy.integrate import solve_ivp

import ladder as ld

# data (same as in the report)
L = 4.0                     # length of the ladder [m]
m = 12.0                    # mass of the ladder [kg]
g = 9.81                    # gravitational acceleration [m/s^2]
mu_true = 0.32              # coefficient of friction for generation [-]
theta0 = np.radians(75.0)   # initial angle of the fall [rad]
frame_rate = 30.0           # frames per second [1/s]

rng = np.random.default_rng(0)

# friction measurements: normal force and pulling force
N_meas = np.arange(100.0, 701.0, 100.0)
F_meas = mu_true * N_meas + rng.normal(0.0, 4.0, N_meas.size)
np.savetxt("measurements_friction.csv",
           np.column_stack([N_meas, F_meas]),
           delimiter=",",
           header="N [N],F [N]",
           comments="",
           fmt="%.1f")
print(f"Wrote {N_meas.size} points to measurements_friction.csv")


# fall measurements: angle from the video until detachment from the wall
def detachment(t, y, L, g):
    return ld.wall_force(y[0], y[1], m, L, g)


detachment.terminal = True
detachment.direction = -1

solution = solve_ivp(ld.ode_rhs,
                     (0.0, 5.0),
                     [theta0, 0.0],
                     args=(L, g),
                     events=detachment,
                     dense_output=True,
                     rtol=1e-10,
                     atol=1e-12)
t_det = solution.t_events[0][0]
t_meas = np.arange(0.0, t_det, 1.0 / frame_rate)
theta_meas = np.degrees(solution.sol(t_meas)[0])
theta_meas = theta_meas + rng.normal(0.0, 0.5, t_meas.size)
np.savetxt("measurements_fall.csv",
           np.column_stack([t_meas, theta_meas]),
           delimiter=",",
           header="t [s],theta [deg]",
           comments="",
           fmt="%.4f,%.2f")
print(f"Wrote {t_meas.size} points to measurements_fall.csv")
