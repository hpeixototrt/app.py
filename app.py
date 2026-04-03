import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Visual da Página (Tema Dark Nativo)
st.set_page_config(
    page_title="Gestão de Filtros TRT",
    page_icon="🚰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização para os Cards (CSS para deixar com cara de Infográfico)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 38px; color: #00d4ff !important; font-weight: bold; }
    div.stDataFrame { border: 1px solid #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão Direta com sua Planilha Google
SHEET_ID = "1XQi3Z4BbYqu9OvZFGsR_gBZo2N68C5KFGMrt4HL-Cok"
# Exportamos como CSV para garantir que o Streamlit leia os dados instantaneamente
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1429723031"

@st.cache_data(ttl=60) # Atualiza o cache a cada 60 segundos
def load_data():
    df = pd.read_csv(CSV_URL)
    # Limpa espaços extras nos nomes das colunas se houver
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    st.title("📊 Painel de Controle: Filtros de Água")
    st.info("Os dados abaixo são lidos em tempo real da sua planilha no Google Drive.")

    # --- LINHA 1: CARDS DE RESUMO (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total de Equipamentos", value=len(df))

    with col2:
        # Conta quantas localidades diferentes existem
        loc_count = df['LOCALIDADE'].nunique() if 'LOCALIDADE' in df.columns else 0
        st.metric(label="Cidades/Unidades", value=loc_count)

    with col3:
        # Exemplo de contagem por situação (ajuste conforme os termos da sua planilha)
        ativos = len(df[df['SITUAÇÃO'].str.contains('ATIVO|INSTALADO', na=False, case=False)]) if 'SITUAÇÃO' in df.columns else "N/A"
        st.metric(label="Filtros Ativos", value=ativos)

    with col4:
        st.metric(label="Status de Atualização", value="Sincronizado", delta="OK")

    st.markdown("---")

    # --- LINHA 2
