"""Точка входа интерфейса: только сборка страницы.

Запуск из корня проекта:
    uv run streamlit run src/grid_ising/ui/app.py
"""
import streamlit as st

from grid_ising.config import DEFAULT_GRAPH, SIM
from grid_ising.ui.components import footer, hero, kpi_row
from grid_ising.ui.services import list_graphs, load_model, simulate
from grid_ising.ui.tabs import render_about_tab, render_map_tab, render_thermo_tab
from grid_ising.ui.theme import apply_theme

st.set_page_config(page_title="Живучесть энергосетей", layout="wide")
apply_theme()
hero()


def sidebar():
    files = list_graphs()
    if not files:
        st.error("В папке data/ нет файлов .graphml. Положите туда данные сети.")
        st.stop()

    with st.sidebar:
        st.markdown("## Параметры")
        graph = st.selectbox(
            "Сеть", files,
            index=files.index(DEFAULT_GRAPH) if DEFAULT_GRAPH in files else 0,
        )
        t_lo, t_hi = st.slider("Диапазон T (в долях T_c)", 0.1, 4.0,
                               (SIM.t_min_factor, SIM.t_max_factor), step=0.05)
        n_temps = st.slider("Точек по температуре", 5, 100, SIM.n_temps)
        steps_thermal = st.slider("Шагов разогрева", 100, 10000,
                                  SIM.steps_thermal, step=100)
        steps_measure = st.slider("Шагов измерения", 100, 20000,
                                  SIM.steps_measure, step=100)
        st.markdown("&nbsp;", unsafe_allow_html=True)
        run = st.button("Запустить расчёт", type="primary", use_container_width=True)
        st.caption("Первый запуск компилирует numba-ядро, это займёт несколько секунд.")

    return graph, (n_temps, steps_thermal, steps_measure, t_lo, t_hi), run


def main():
    graph, params, run = sidebar()
    model = load_model(graph)

    kpi_row([
        ("Узлов", f"{model.num_nodes:,}", "подстанции"),
        ("Рёбер", f"{model.num_edges:,}", "линии электропередачи"),
        ("Средняя степень ⟨k⟩", f"{model.mean_degree:.2f}", "связность узла"),
        ("T_c теор.", f"{2.0 / model.mean_degree:.3f}", "оценка 2 / ⟨k⟩"),
    ])

    if run:
        with st.spinner("Считаем методом Монте-Карло…"):
            temps, e, C, Tc = simulate(graph, *params)
        st.session_state["result"] = dict(graph=graph, temps=temps, e=e, C=C, Tc=Tc)

    result = st.session_state.get("result")
    if result is not None and result["graph"] != graph:
        result = None  # результат относится к другой сети

    tab1, tab2, tab3 = st.tabs(["Термодинамика", "Карта сети", "О модели"])
    with tab1:
        render_thermo_tab(graph, result)
    with tab2:
        render_map_tab(graph, model, result)
    with tab3:
        render_about_tab()

    footer()


main()