from simulation import simulate_mass_spring_damper
from plotting import plot_single_case, plot_damping_comparison


def main():
    # parametri sistem
    m = 1.0
    k = 10.0
    x0 = 1.0
    v0 = 0.0
    t_max = 10.0
    dt = 0.01

    damping_values = [0.2, 0.8, 5.0]

    # grafic comparativ pentru cele 3 amortizări
    plot_damping_comparison(m, k, x0, v0, t_max, dt, damping_values)

    # exemplu pentru un singur caz
    c = 0.8
    t_values, x_values, v_values = simulate_mass_spring_damper(m, c, k, x0, v0, t_max, dt)
    plot_single_case(t_values, x_values, v_values)


if __name__ == "__main__":
    main()