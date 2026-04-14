import numpy as np


def simulate_mass_spring_damper(m, c, k, x0, v0, t_max, dt):
    """
    Simulează sistemul masă-arc-amortizor folosind metoda Euler.

    Parametri:
        m     - masa
        c     - coeficient de amortizare
        k     - constanta arcului
        x0    - poziția inițială
        v0    - viteza inițială
        t_max - timpul total de simulare
        dt    - pasul de timp

    Returnează:
        t_values - vectorul de timp
        x_values - vectorul pozițiilor
        v_values - vectorul vitezelor
    """

    n_steps = int(t_max / dt) + 1

    t_values = np.zeros(n_steps)
    x_values = np.zeros(n_steps)
    v_values = np.zeros(n_steps)

    x_values[0] = x0
    v_values[0] = v0

    for i in range(n_steps - 1):
        t_values[i + 1] = t_values[i] + dt

        x = x_values[i]
        v = v_values[i]

        dx_dt = v
        dv_dt = -(c / m) * v - (k / m) * x

        x_values[i + 1] = x + dt * dx_dt
        v_values[i + 1] = v + dt * dv_dt

    return t_values, x_values, v_values