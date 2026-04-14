import matplotlib.pyplot as plt
from simulation import simulate_mass_spring_damper


def plot_single_case(t_values, x_values, v_values):
    """
    Afișează poziția și viteza pentru un singur caz.
    """
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(t_values, x_values, label="Poziție x(t)")
    plt.xlabel("Timp [s]")
    plt.ylabel("Poziție [m]")
    plt.title("Evoluția poziției în timp")
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(t_values, v_values, label="Viteză v(t)")
    plt.xlabel("Timp [s]")
    plt.ylabel("Viteză [m/s]")
    plt.title("Evoluția vitezei în timp")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_damping_comparison(m, k, x0, v0, t_max, dt, damping_values):
    """
    Compară evoluția poziției pentru mai multe valori ale amortizării.
    """
    plt.figure(figsize=(10, 6))

    for c in damping_values:
        t_values, x_values, _ = simulate_mass_spring_damper(m, c, k, x0, v0, t_max, dt)
        plt.plot(t_values, x_values, label=f"c = {c}")

    plt.xlabel("Timp [s]")
    plt.ylabel("Poziție [m]")
    plt.title("Comparație între diferite valori ale amortizării")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()