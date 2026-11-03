from numba import njit
import numpy as np

@njit
def calculate_energy_graph(spins, neighbors_indices, neighbors_weights):
    energy = 0.0
    for i in range(len(spins)):
        local_sum = 0.0
        neighs = neighbors_indices[i]
        weights = neighbors_weights[i]
        for k in range(len(neighs)):
            local_sum += weights[k] * spins[neighs[k]]
        energy += -spins[i] * local_sum
    return energy / 2.0

@njit
def metropolis_step_graph(spins, temperature, neighbors_indices, neighbors_weights):
    N = len(spins)
    for _ in range(N):
        i = np.random.randint(0, N)
        local_field = 0.0
        neighs = neighbors_indices[i]
        weights = neighbors_weights[i]
        for k in range(len(neighs)):
            local_field += weights[k] * spins[neighs[k]]
            
        dE = 2.0 * spins[i] * local_field
        if dE < 0 or np.random.rand() < np.exp(-dE / temperature):
            spins[i] *= -1