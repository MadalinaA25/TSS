import numpy as np
import math


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


class MassSpringDamper:
    """
    Clasa care modeleaza un sistem masa-arc-amortizor.
    Permite configurarea parametrilor fizici, determinarea tipului de amortizare
    si rularea simularii numerice prin metoda Euler.
    """

    def __init__(self, m, c, k):
        """
        Initializeaza sistemul cu parametrii fizici.

        Parametri:
            m - masa [kg] (trebuie sa fie strict pozitiva)
            c - coeficient de amortizare [N*s/m] (trebuie sa fie nenegativ)
            k - constanta arcului [N/m] (trebuie sa fie strict pozitiva)

        Ridica:
            ValueError daca m <= 0, c < 0 sau k <= 0
        """
        if m <= 0:
            raise ValueError("Masa m trebuie sa fie strict pozitiva")
        if c < 0:
            raise ValueError("Coeficientul de amortizare c trebuie sa fie nenegativ")
        if k <= 0:
            raise ValueError("Constanta arcului k trebuie sa fie strict pozitiva")
        self.m = m
        self.c = c
        self.k = k

    def get_damping_type(self):
        """
        Calculeaza factorul de amortizare zeta si returneaza tipul de amortizare.

        Returneaza:
            'subdampat'   daca zeta < 1
            'critic'      daca zeta == 1
            'supradampat' daca zeta > 1
        """
        zeta = self.c / (2 * math.sqrt(self.m * self.k))
        if zeta < 1:
            return "subdampat"
        elif zeta == 1:
            return "critic"
        else:
            return "supradampat"

    def simulate(self, x0, v0, t_max, dt):
        """
        Ruleaza simularea numerica a sistemului folosind metoda Euler.

        Parametri:
            x0    - pozitia initiala [m]
            v0    - viteza initiala [m/s]
            t_max - durata simularii [s] (trebuie sa fie strict pozitiva)
            dt    - pasul de timp [s] (trebuie sa fie strict pozitiv si mai mic decat t_max)

        Returneaza:
            t_values, x_values, v_values

        Ridica:
            ValueError daca t_max <= 0, dt <= 0 sau dt >= t_max
        """
        if t_max <= 0:
            raise ValueError("t_max trebuie sa fie strict pozitiv")
        if dt <= 0:
            raise ValueError("dt trebuie sa fie strict pozitiv")
        if dt >= t_max:
            raise ValueError("dt trebuie sa fie mai mic decat t_max")
        return simulate_mass_spring_damper(self.m, self.c, self.k, x0, v0, t_max, dt)
