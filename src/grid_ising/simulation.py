import numpy as np

from grid_ising.core.physics import calculate_energy_graph, metropolis_step_graph


def run_simulation(model, temperatures, steps_thermal, steps_measure, verbose=True):
    """Для каждой температуры возвращает <E> и <E^2> (полные, не на узел)."""
    N = model.num_nodes
    mean_E = np.zeros(len(temperatures))
    mean_E2 = np.zeros(len(temperatures))

    for k, T in enumerate(temperatures):
        spins = np.random.choice([-1, 1], size=N).astype(np.int64)

        for _ in range(steps_thermal):
            metropolis_step_graph(spins, T, model.neighbors_indices, model.neighbors_weights)

        Es = np.empty(steps_measure)
        for s in range(steps_measure):
            metropolis_step_graph(spins, T, model.neighbors_indices, model.neighbors_weights)
            Es[s] = calculate_energy_graph(spins, model.neighbors_indices, model.neighbors_weights)

        mean_E[k] = Es.mean()
        mean_E2[k] = (Es ** 2).mean()

        if verbose:
            print(f"T = {T:.2f} | <E>/N = {mean_E[k] / N:.3f}")

    return mean_E, mean_E2