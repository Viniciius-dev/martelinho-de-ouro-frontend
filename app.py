"""
🔧 Martelinho de Ouro — Sistema de Gestão
Execute com: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="Martelinho de Ouro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

.block-container { padding-top: 2rem; }

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
div[data-testid="stMetric"] label { color: #8b8ba7 !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e94560 !important; }

h1 {
    background: linear-gradient(90deg, #e94560, #533483, #0f3460);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #e94560, #533483) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    width: 100% !important; /* Botões sempre amigáveis ao toque e responsivos */
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(233,69,96,0.4) !important;
}

div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; width: 100% !important; }

/* Melhorias de Responsividade para Celulares e Tablets */
@media screen and (max-width: 768px) {
    .block-container { 
        padding-top: 1rem !important; 
        padding-left: 0.8rem !important; 
        padding-right: 0.8rem !important; 
    }
    h1 { font-size: 1.8rem !important; }
    div[data-testid="stMetric"] { 
        padding: 10px !important; 
        margin-bottom: 10px !important; 
    }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔧 Martelinho de Ouro")
    st.markdown("*Sistema de Gestão*")
    st.markdown("---")
    pagina = st.radio(
        "Menu",
        [
            "📊 Dashboard",
            "📦 Estoque de Peças",
            "🛒 Registrar Compra",
            "💰 Registrar Venda",
            "📈 Relatórios",
            "⚙️ Área Administrativa",
            "📜 Histórico do Sistema",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;font-size:11px;opacity:0.4'>"
        "Martelinho de Ouro v1.0</div>",
        unsafe_allow_html=True,
    )

from ui_pages import (
    pagina_dashboard, pagina_estoque, pagina_compra,
    pagina_venda, pagina_relatorios, pagina_gerar_dados,
    pagina_historico_logs
)

rotas = {
    "📊 Dashboard": pagina_dashboard,
    "📦 Estoque de Peças": pagina_estoque,
    "🛒 Registrar Compra": pagina_compra,
    "💰 Registrar Venda": pagina_venda,
    "📈 Relatórios": pagina_relatorios,
    "⚙️ Área Administrativa": pagina_gerar_dados,
    "📜 Histórico do Sistema": pagina_historico_logs,
}

rotas[pagina]()
