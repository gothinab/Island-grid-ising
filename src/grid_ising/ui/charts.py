"""Построение фигур Plotly. Принимают готовые данные, ничего не считают."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from grid_ising.ui.services import edge_lines, node_positions
from grid_ising.ui.theme import (
    CARD, CORAL, GRID, GRID_MINOR, INK, MUTED, SAGE, SPIKE, TERRACOTTA,
)

FONT = "Montserrat, sans-serif"
HOVERLABEL = dict(bgcolor=CARD, bordercolor=TERRACOTTA,
                  font=dict(family=FONT, size=13, color=INK))


def style_axes(fig):
    """Сетка и перекрестие (crosshair), следующее за курсором."""
    axis = dict(
        showgrid=True, gridcolor=GRID, gridwidth=1,
        zeroline=False, showline=True, linecolor="rgba(58,47,44,0.35)",
        ticks="outside", tickcolor="rgba(58,47,44,0.35)",
        tickfont=dict(color=MUTED),
        showspikes=True, spikemode="across", spikesnap="cursor",
        spikethickness=1, spikedash="dot", spikecolor=SPIKE,
        minor=dict(showgrid=True, gridcolor=GRID_MINOR),
    )
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)


def thermo_figure(temps, e, C, Tc):
    fig = make_subplots(
        rows=1, cols=2, horizontal_spacing=0.09,
        subplot_titles=("Энергия на узел  ⟨E⟩/N", "Теплоёмкость на узел  C/N"),
    )

    fig.add_trace(go.Scatter(
        x=temps, y=e, mode="lines+markers", name="E/N",
        line=dict(color=SAGE, width=2.5),
        marker=dict(size=7, color=CARD, line=dict(color=SAGE, width=2)),
        fill="tozeroy", fillcolor="rgba(129,159,167,0.14)",
        hovertemplate="T = %{x:.3f}<br>⟨E⟩/N = %{y:.4f}<extra></extra>",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=temps, y=C, mode="lines+markers", name="C/N",
        line=dict(color=TERRACOTTA, width=2.5),
        marker=dict(size=7, color=CARD, line=dict(color=TERRACOTTA, width=2)),
        fill="tozeroy", fillcolor="rgba(173,69,58,0.09)",
        hovertemplate="T = %{x:.3f}<br>C/N = %{y:.4f}<extra></extra>",
    ), row=1, col=2)

    k = int(np.argmax(C))
    fig.add_trace(go.Scatter(
        x=[temps[k]], y=[C[k]], mode="markers", name="Пик C",
        marker=dict(size=13, color=INK, symbol="diamond",
                    line=dict(color=CARD, width=1.5)),
        hovertemplate="Пик C<br>T = %{x:.3f}<br>C/N = %{y:.4f}<extra></extra>",
    ), row=1, col=2)

    for col in (1, 2):
        fig.add_vline(
            x=Tc, line_dash="dash", line_color=CORAL, line_width=1.8, row=1, col=col,
            annotation_text=f"T_c теор. ≈ {Tc:.2f}", annotation_position="top right",
            annotation_font=dict(color=TERRACOTTA, size=11),
        )

    style_axes(fig)
    fig.update_xaxes(title_text="Температура T", title_font=dict(color=MUTED, size=12))
    fig.update_layout(
        height=470, showlegend=False, template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=INK, size=13),
        margin=dict(l=20, r=20, t=60, b=40),
        hovermode="closest", hoverdistance=60, spikedistance=-1,
        hoverlabel=HOVERLABEL,
    )
    fig.update_annotations(font=dict(size=14, color=INK))
    return fig


def network_figure(name, spins):
    xy, geo = node_positions(name)
    ex, ey = edge_lines(name)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ex, y=ey, mode="lines", hoverinfo="skip",
        line=dict(color="rgba(138,118,109,0.40)", width=1),
    ))
    for val, color, label in ((1, SAGE, "работает (+1)"), (-1, TERRACOTTA, "отказал (−1)")):
        mask = spins == val
        fig.add_trace(go.Scatter(
            x=xy[mask, 0], y=xy[mask, 1], mode="markers", name=label,
            marker=dict(size=9, color=color, line=dict(color=CARD, width=1)),
            hovertemplate=f"{label}<extra></extra>",
        ))

    yaxis = dict(visible=False)
    if geo and abs(float(np.mean(xy[:, 1]))) < 85:
        yaxis.update(scaleanchor="x",
                     scaleratio=1.0 / np.cos(np.radians(np.mean(xy[:, 1]))))
    fig.update_layout(
        height=620, template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=INK),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False), yaxis=yaxis,
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center",
                    bgcolor="rgba(0,0,0,0)"),
        hoverlabel=HOVERLABEL,
    )
    return fig