"""Небольшие переиспользуемые блоки интерфейса."""
import streamlit as st


def kpi(label, value, sub=""):
    return (f'<div class="kpi"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="sub">{sub}</div></div>')


def kpi_row(items):
    """items: список кортежей (label, value, sub). Рисует ряд карточек."""
    cols = st.columns(len(items))
    for col, (label, value, sub) in zip(cols, items):
        col.markdown(kpi(label, value, sub), unsafe_allow_html=True)


def section(title, subtitle=""):
    st.markdown(f'<div class="section-title">{title}</div>'
                f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def hero():
    st.markdown(
        """
<div class="hero">
  <div class="eyebrow">Модель Изинга · высоковольтные сети</div>
  <h1>Живучесть энергосетей</h1>
  <p>Каждая подстанция представлена спином Изинга: она либо работает, либо отказала.
  Температура задаёт уровень технологического шума, а фазовый переход
  показывает, при каком шуме сеть теряет согласованность.</p>
</div>
""",
        unsafe_allow_html=True,
    )


def footer():
    st.markdown('<div class="foot">grid-ising · метод Монте-Карло (Метрополис) на графе '
                'реальной энергосети</div>', unsafe_allow_html=True)