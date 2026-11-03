from dataclasses import dataclass
from pathlib import Path

# config.py лежит в src/grid_ising/, корень проекта на два уровня выше
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

DEFAULT_GRAPH = "Denmark_highvoltage.graphml"


@dataclass(frozen=True)
class SimulationConfig:
    n_temps: int = 30
    steps_thermal: int = 2000
    steps_measure: int = 3000
    t_min_factor: float = 0.2   # T_min = t_min_factor * Tc
    t_max_factor: float = 2.0   # T_max = t_max_factor * Tc
    seed: int | None = None     # None = каждый раз разные результаты


@dataclass(frozen=True)
class PlotConfig:
    figsize: tuple = (14, 5)
    dpi: int = 150
    energy_color: str = "blue"
    heat_capacity_color: str = "crimson"
    tc_color: str = "red"


SIM = SimulationConfig()
PLOT = PlotConfig()