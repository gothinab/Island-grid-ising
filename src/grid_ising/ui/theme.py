import streamlit as st

# палитра
TERRACOTTA = "#ad453a"
CREAM = "#f3ece4"
CORAL = "#d88b79"
SAGE = "#819fa7"
BLUSH = "#d9b6a3"

# производные тона
INK = "#3a2f2c"        # основной текст
MUTED = "#8a766d"      # второстепенный текст
CARD = "#faf5ee"       # фон карточек и графиков
LINE = "#e2d4c7"       # тонкие границы
SIDEBAR = "#ede2d6"

GRID = "rgba(58,47,44,0.10)"
GRID_MINOR = "rgba(58,47,44,0.05)"
SPIKE = "rgba(58,47,44,0.55)"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Montserrat', sans-serif; color: #3a2f2c; }
.stApp { background: #f3ece4; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.4rem; max-width: 1280px; }

h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; color: #3a2f2c; letter-spacing: -0.01em; }

/* шапка */
.hero { padding: 0 0 1.6rem 0; margin-bottom: 1.4rem; border-bottom: 1px solid #e2d4c7; }
.hero .eyebrow {
    font-size: .74rem; font-weight: 600; letter-spacing: .14em;
    text-transform: uppercase; color: #ad453a;
}
.hero h1 { margin: .5rem 0 .7rem 0; font-size: 2.4rem; font-weight: 700; color: #3a2f2c; }
.hero p { margin: 0; color: #7a665d; font-size: 1rem; max-width: 760px; line-height: 1.7; }

/* карточки */
.kpi {
    padding: 16px 18px; border-radius: 10px;
    background: #faf5ee; border: 1px solid #e2d4c7;
}
.kpi .label { color: #8a766d; font-size: .72rem; font-weight: 600; letter-spacing: .09em; text-transform: uppercase; }
.kpi .value { color: #3a2f2c; font-size: 1.7rem; font-weight: 600; margin-top: 6px; }
.kpi .sub   { color: #a8948a; font-size: .8rem; margin-top: 2px; }

.section-title { font-size: 1.1rem; font-weight: 600; color: #3a2f2c; margin: 1.5rem 0 .2rem 0; }
.section-sub   { color: #8a766d; font-size: .88rem; margin-bottom: .7rem; line-height: 1.55; }

/* боковая панель */
section[data-testid="stSidebar"] { background: #ede2d6; border-right: 1px solid #e2d4c7; }
section[data-testid="stSidebar"] h2 { font-size: 1rem; font-weight: 600; }

/* кнопки */
.stButton > button[kind="primary"], .stDownloadButton > button {
    border: 0; border-radius: 8px; font-weight: 600; padding: .6rem 1rem;
    background: #ad453a; color: #f3ece4;
    transition: background .15s ease;
}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {
    background: #953a31; color: #f3ece4;
}

/* вкладки */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #e2d4c7; }
.stTabs [data-baseweb="tab"] { height: 44px; padding: 0 16px; color: #8a766d; font-weight: 500; }
.stTabs [aria-selected="true"] { color: #ad453a !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #ad453a; }

/* информационные блоки */
div[data-testid="stAlert"] {
    background: #ede2d6; border: 1px solid #e2d4c7; color: #3a2f2c; border-radius: 10px;
}

/* графики */
div[data-testid="stPlotlyChart"] {
    border-radius: 12px; padding: 8px;
    background: #faf5ee; border: 1px solid #e2d4c7;
}
.foot { color: #a8948a; font-size: .8rem; text-align: center; margin-top: 2.4rem; }
</style>
"""


def apply_theme():
    st.markdown(_CSS, unsafe_allow_html=True)