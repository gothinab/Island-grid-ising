import argparse

import networkx as nx
import numpy as np

from grid_ising.config import DATA_DIR, RESULTS_DIR, DEFAULT_GRAPH, SIM
from grid_ising.data_io.loader import NetworkFaultTolerance
from grid_ising.simulation import run_simulation
from grid_ising.visualization.plots import plot_thermodynamics


def main():
    parser = argparse.ArgumentParser(description="Модель Изинга на графе энергосети")
    parser.add_argument("--graph", default=DEFAULT_GRAPH)
    parser.add_argument("--n-temps", type=int, default=SIM.n_temps)
    parser.add_argument("--steps-thermal", type=int, default=SIM.steps_thermal)
    parser.add_argument("--steps-measure", type=int, default=SIM.steps_measure)
    parser.add_argument("--seed", type=int, default=SIM.seed)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)

    G = nx.read_graphml(DATA_DIR / args.graph)
    model = NetworkFaultTolerance(G)

    Tc = 2.0 / model.mean_degree
    temps = np.linspace(SIM.t_min_factor * Tc, SIM.t_max_factor * Tc, args.n_temps)

    mean_E, mean_E2 = run_simulation(model, temps, args.steps_thermal, args.steps_measure)

    N = model.num_nodes
    e_per_node = mean_E / N
    C_per_node = (mean_E2 - mean_E ** 2) / (temps ** 2 * N)

    name = args.graph.rsplit(".", 1)[0]
    plot_thermodynamics(
        temps, e_per_node, C_per_node, Tc,
        save_path=RESULTS_DIR / f"{name}_thermo.png",
        show=not args.no_show,
    )


if __name__ == "__main__":
    main()