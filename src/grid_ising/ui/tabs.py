"""Содержимое вкладок. Каждая функция отрисовывает одну вкладку."""
import io

import numpy as np
import streamlit as st

from grid_ising.ui.charts import network_figure, thermo_figure
from grid_ising.ui.components import kpi_row, section
from grid_ising.ui.services import node_positions, relax


def render_thermo_tab(graph, result):
    if result is None:
        st.info("Выберите параметры слева и нажмите «Запустить расчёт».")
        return

    temps, e, C, Tc = result["temps"], result["e"], result["C"], result["Tc"]
    T_peak = float(temps[int(np.argmax(C))])

    kpi_row([
        ("Пик теплоёмкости", f"{T_peak:.3f}", "T_c по симуляции"),
        ("Теория", f"{Tc:.3f}", "T_c ≈ 2 / ⟨k⟩"),
        ("Расхождение", f"{abs(T_peak - Tc) / Tc * 100:.1f}%", "симуляция против теории"),
    ])

    section("Фазовый переход",
            "Наведите курсор: перекрестие показывает точные значения T и величины. "
            "Колесо мыши — масштаб, двойной клик — сброс.")
    st.plotly_chart(
        thermo_figure(temps, e, C, Tc), use_container_width=True,
        config=dict(displaylogo=False, modeBarButtonsToRemove=["lasso2d", "select2d"],
                    toImageButtonOptions=dict(format="png", scale=2,
                                              filename="ising_thermo")),
    )

    buf = io.StringIO()
    np.savetxt(buf, np.column_stack([temps, e, C]), delimiter=",",
               header="T,E_per_node,C_per_node", comments="")
    st.download_button("Скачать данные (CSV)", buf.getvalue(),
                       file_name=f"{graph.rsplit('.', 1)[0]}_thermo.csv",
                       mime="text/csv")


def render_map_tab(graph, model, result):
    section("Состояние сети при выбранной температуре",
            "Двигайте ползунок: при низкой T почти все узлы согласованы, возле T_c "
            "появляются кластеры отказов, при высокой T картина превращается в шум.")

    Tc0 = 2.0 / model.mean_degree
    if result is not None:
        lo, hi = float(result["temps"].min()), float(result["temps"].max())
        default_T = float(result["temps"][int(np.argmax(result["C"]))])
    else:
        lo, hi, default_T = 0.2 * Tc0, 2.0 * Tc0, Tc0

    c_a, c_b = st.columns([3, 1])
    T_map = c_a.slider("Температура T", lo, hi, default_T, step=(hi - lo) / 100,
                       format="%.3f")
    relax_steps = c_b.slider("Шагов релаксации", 50, 5000, 500, step=50)

    spins = relax(graph, round(float(T_map), 4), relax_steps)

    kpi_row([
        ("Магнитизация |m|", f"{abs(float(spins.mean())):.3f}",
         "1 — полный порядок, 0 — хаос"),
        ("Работают", f"{int((spins == 1).sum()):,}", "узлов со спином +1"),
        ("Отказали", f"{int((spins == -1).sum()):,}", "узлов со спином −1"),
    ])

    st.plotly_chart(network_figure(graph, spins), use_container_width=True,
                    config=dict(displaylogo=False))

    _, geo = node_positions(graph)
    if not geo:
        st.caption("В graphml не нашлись географические координаты, поэтому узлы "
                   "размещены автоматически (spring layout).")


def render_about_tab():
    st.markdown("### Модель")
    st.latex(r"H = -J \sum_{\langle i,j\rangle} s_i s_j, \qquad s_i = \pm 1")
    st.markdown(
        "- **+1** — подстанция работает, **−1** — отказала.\n"
        "- Рёбра графа — линии электропередачи, они задают взаимодействие.\n"
        "- Динамика — алгоритм Метрополиса: переворот спина принимается, если "
        "энергия падает, либо с вероятностью $e^{-\\Delta E / T}$."
    )
    st.markdown("### Наблюдаемые")
    st.latex(r"C = \frac{\langle E^2\rangle - \langle E\rangle^2}{N\,T^2}")
    st.markdown(
        "Критическая температура $T_c$ соответствует пику теплоёмкости. "
        "Для сравнения используется оценка теории среднего поля, "
        "$T_c \\approx 2/\\langle k\\rangle$."
    )