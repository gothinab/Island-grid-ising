from pathlib import Path
import matplotlib.pyplot as plt
from grid_ising.config import PLOT


def plot_energy(ax, temperatures, e_per_node, Tc_theory):
    ax.plot(temperatures, e_per_node, 'o-', color=PLOT.energy_color)
    ax.axvline(Tc_theory, ls='--', color=PLOT.tc_color,
            label=f'Теор. $T_c \\approx$ {Tc_theory:.2f}')
    ax.set_xlabel("Температура (T)")
    ax.set_ylabel("Энергия на узел $\\langle E \\rangle / N$")
    ax.set_title("Энергия от температуры")
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_heat_capacity(ax, temperatures, C_per_node, Tc_theory):
    ax.plot(temperatures, C_per_node, 'o-', color=PLOT.heat_capacity_color)
    ax.axvline(Tc_theory, ls='--', color=PLOT.tc_color)
    ax.set_xlabel("Температура (T)")
    ax.set_ylabel("Теплоемкость на узел $C / N$")
    ax.set_title("Теплоемкость от температуры")
    ax.grid(True, alpha=0.3)


def plot_thermodynamics(temperatures, e_per_node, C_per_node, Tc_theory,
                        save_path=None, show=True):
    """Рисует оба графика рядом. Возвращает fig."""
    fig, ax = plt.subplots(1, 2, figsize=PLOT.figsize)

    plot_energy(ax[0], temperatures, e_per_node, Tc_theory)
    plot_heat_capacity(ax[1], temperatures, C_per_node, Tc_theory)

    fig.tight_layout()

    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=PLOT.dpi)

    if show:
        plt.show()

    return fig