"""Загрузка данных и вычисления с кэшированием. Без отрисовки."""
import networkx as nx
import numpy as np
import streamlit as st

from grid_ising.config import DATA_DIR
from grid_ising.core.physics import metropolis_step_graph
from grid_ising.data_io.loader import NetworkFaultTolerance
from grid_ising.simulation import run_simulation


def list_graphs():
    return sorted(p.name for p in DATA_DIR.glob("*.graphml"))


@st.cache_resource
def load_model(name):
    return NetworkFaultTolerance(nx.read_graphml(DATA_DIR / name))


@st.cache_data(show_spinner=False)
def simulate(name, n_temps, steps_thermal, steps_measure, t_lo, t_hi):
    model = load_model(name)
    Tc = 2.0 / model.mean_degree
    temps = np.linspace(t_lo * Tc, t_hi * Tc, n_temps)
    mean_E, mean_E2 = run_simulation(model, temps, steps_thermal, steps_measure,
                                     verbose=False)
    N = model.num_nodes
    e = mean_E / N
    C = (mean_E2 - mean_E ** 2) / (temps ** 2 * N)
    return temps, e, C, Tc


@st.cache_data(show_spinner=False)
def relax(name, T, steps):
    model = load_model(name)
    spins = np.random.choice([-1, 1], size=model.num_nodes).astype(np.int64)
    for _ in range(steps):
        metropolis_step_graph(spins, T, model.neighbors_indices, model.neighbors_weights)
    return spins


@st.cache_data(show_spinner=False)
def node_positions(name):
    model = load_model(name)
    G = model.network_graph
    for kx, ky in [("lon", "lat"), ("longitude", "latitude"), ("Longitude", "Latitude"),
                   ("x", "y"), ("X", "Y")]:
        if all(kx in G.nodes[n] and ky in G.nodes[n] for n in model.nodes):
            try:
                xy = np.array([[float(G.nodes[n][kx]), float(G.nodes[n][ky])]
                               for n in model.nodes])
                return xy, True
            except ValueError:
                pass
    pos = nx.spring_layout(G, seed=7)
    return np.array([pos[n] for n in model.nodes]), False


@st.cache_data(show_spinner=False)
def edge_lines(name):
    model = load_model(name)
    xy, _ = node_positions(name)
    idx = {n: i for i, n in enumerate(model.nodes)}
    xs, ys = [], []
    for u, v in model.network_graph.edges():
        a, b = idx[u], idx[v]
        xs += [xy[a, 0], xy[b, 0], None]
        ys += [xy[a, 1], xy[b, 1], None]
    return xs, ys
