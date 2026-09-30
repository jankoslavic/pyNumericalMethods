"""
Ladder against a smooth wall: statics (slipping) and dynamics of the fall.

The module collects the functions that the report uses more than once:
the matrix and the right-hand side of the equilibrium equations, the
critical position of the person and the critical angle, the angular
velocity of the fall from energy, the wall force during the fall, the
right-hand side of the differential equation of the fall and our own
Euler method.

Notation: theta is the angle of the ladder from the floor [rad], L the
length of the ladder [m], m the mass of the ladder [kg], m_p the mass of
the person [kg], x the position of the person from the lower end [m],
mu the coefficient of friction on the floor [-], g the gravitational
acceleration [m/s^2].
The functions do not plot or print; they only return numerical results.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def equilibrium_matrix(theta: float, L: float) -> np.ndarray:
    """
    Matrix of the ladder's equilibrium equations for unknowns [F_A, N_A, N_B].

    The rows are the sum of forces in x, the sum of forces in y and the
    sum of moments about the lower end A. The matrix depends only on the
    angle of the ladder.

    Parameters
    ----------
    theta : float
        Angle of the ladder from the floor [rad].
    L : float
        Length of the ladder [m].

    Returns
    -------
    ndarray, shape (3, 3)
        System matrix.
    """
    A = np.array([[1.0, 0.0, -1.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, L * np.sin(theta)]])
    return A


def right_hand_side(theta: float, x: float, m: float, m_p: float,
                    L: float, g: float) -> np.ndarray:
    """
    Right-hand side of the equilibrium equations (loads).

    Parameters
    ----------
    theta : float
        Angle of the ladder from the floor [rad].
    x : float
        Position of the person from the lower end [m].
    m, m_p : float
        Mass of the ladder and mass of the person [kg].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray, shape (3,)
        Right-hand side vector [N, N, N m].
    """
    moment = (m * L / 2 + m_p * x) * g * np.cos(theta)
    b = np.array([0.0, (m + m_p) * g, moment])
    return b


def critical_position(theta: float, mu: float, m: float, m_p: float,
                      L: float) -> float:
    """
    Position of the person at which the ladder starts to slip (F_A = mu N_A).

    Parameters
    ----------
    theta : float
        Angle of the ladder from the floor [rad].
    mu : float
        Coefficient of friction between the ladder and the floor [-].
    m, m_p : float
        Mass of the ladder and mass of the person [kg].
    L : float
        Length of the ladder [m].

    Returns
    -------
    float
        Critical position x_cr [m]; it can also lie outside [0, L].
    """
    x_cr = (mu * (m + m_p) * L * np.tan(theta) - m * L / 2) / m_p
    return x_cr


def critical_angle(mu: float) -> float:
    """
    Smallest angle at which the ladder without a person does not slip yet.

    Parameters
    ----------
    mu : float
        Coefficient of friction between the ladder and the floor [-].

    Returns
    -------
    float
        Critical angle [rad], tan(theta_cr) = 1 / (2 mu).
    """
    return np.arctan(1.0 / (2.0 * mu))


def omega_energy(theta: np.ndarray, theta0: float, L: float,
                 g: float) -> np.ndarray:
    """
    Angular velocity of the falling ladder from conservation of energy.

    Valid for a frictionless ladder that touches the floor and the wall
    and was released from rest at the angle theta0.

    Parameters
    ----------
    theta : ndarray
        Angle of the ladder [rad], theta <= theta0.
    theta0 : float
        Initial angle [rad].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray
        Magnitude of the angular velocity [rad/s].
    """
    return np.sqrt(3.0 * g / L * (np.sin(theta0) - np.sin(theta)))


def angular_acceleration(theta: np.ndarray, L: float,
                         g: float) -> np.ndarray:
    """
    Angular acceleration of the falling frictionless ladder.

    Parameters
    ----------
    theta : ndarray
        Angle of the ladder [rad].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray
        Angular acceleration [rad/s^2].
    """
    return -3.0 * g / (2.0 * L) * np.cos(theta)


def wall_force(theta: np.ndarray, omega: np.ndarray, m: float,
               L: float, g: float) -> np.ndarray:
    """
    Force of the smooth wall on the ladder during the fall from the current state.

    Follows from N_B = m * d^2 x_G / dt^2 with x_G = L/2 cos(theta).

    Parameters
    ----------
    theta, omega : ndarray
        Angle [rad] and angular velocity [rad/s] of the ladder.
    m : float
        Mass of the ladder [kg].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray
        Wall force N_B [N]; a negative value means detachment.
    """
    alpha = angular_acceleration(theta, L, g)
    acceleration_x = -L / 2 * (np.cos(theta) * omega**2 + np.sin(theta) * alpha)
    return m * acceleration_x


def wall_force_energy(theta: np.ndarray, theta0: float, m: float,
                      g: float) -> np.ndarray:
    """
    Force of the smooth wall as a function of the angle (angular velocity from energy).

    Parameters
    ----------
    theta : ndarray
        Angle of the ladder [rad].
    theta0 : float
        Initial angle [rad].
    m : float
        Mass of the ladder [kg].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray
        Wall force N_B [N].
    """
    factor = 3.0 * np.sin(theta) - 2.0 * np.sin(theta0)
    return 3.0 * m * g / 4.0 * np.cos(theta) * factor


def detachment_angle(theta0: float) -> float:
    """
    Angle at which the upper end of the ladder detaches from the wall.

    Parameters
    ----------
    theta0 : float
        Initial angle [rad].

    Returns
    -------
    float
        Detachment angle [rad], sin(theta_det) = 2/3 sin(theta0).
    """
    return np.arcsin(2.0 / 3.0 * np.sin(theta0))


def time_integrand(theta: np.ndarray, theta0: float, L: float,
                   g: float) -> np.ndarray:
    """
    Integrand for the fall time, dt/dtheta = 1 / omega(theta).

    Parameters
    ----------
    theta : ndarray
        Angle of the ladder [rad], theta < theta0.
    theta0 : float
        Initial angle [rad].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray
        Value of the integrand [s/rad]; it is singular at theta0.
    """
    return 1.0 / omega_energy(theta, theta0, L, g)


def ode_rhs(t: float, y: np.ndarray, L: float, g: float) -> np.ndarray:
    """
    Right-hand side of the first-order system for the frictionless fall of the ladder.

    The state is y = [theta, omega].

    Parameters
    ----------
    t : float
        Time [s]; it does not appear in the equation.
    y : ndarray, shape (2,)
        Angle [rad] and angular velocity [rad/s].
    L : float
        Length of the ladder [m].
    g : float
        Gravitational acceleration [m/s^2].

    Returns
    -------
    ndarray, shape (2,)
        Derivative of the state [rad/s, rad/s^2].
    """
    theta, omega = y
    return np.array([omega, angular_acceleration(theta, L, g)])


def euler(f: Callable, y0: np.ndarray, t: np.ndarray,
          args: tuple = ()) -> np.ndarray:
    """
    Explicit Euler method for the system y' = f(t, y).

    Parameters
    ----------
    f : callable
        Right-hand side f(t, y, *args), returns an ndarray of the shape of y.
    y0 : ndarray
        Initial state.
    t : ndarray
        Time points (uniform or not).
    args : tuple
        Additional arguments for f.

    Returns
    -------
    ndarray, shape (len(t), len(y0))
        Solution at the time points.
    """
    y = np.zeros((t.size, np.size(y0)))
    y[0] = y0
    for i in range(t.size - 1):
        dt = t[i + 1] - t[i]
        y[i + 1] = y[i] + dt * f(t[i], y[i], *args)
    return y
