import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard Filtros TRT", layout="wide")

# 2. Link da Planilha (CSV)
SHEET_ID = "1XQi3Z4BbYqu9OvZFGsR_gBZo2N68C5KFGMrt4HL-Cok"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1429723031"

def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler planilha: {e}")
        return None

# 3. Execução do Dashboard
df = load_data()

if df is not None:
    st.title("📊 Gestão de Filtros - TRT")
    st.markdown("---")

    # CARDS (KPIs)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Filtros", len(df))
    if 'LOCALIDADE' in df.columns:
        c2.metric("Localidades", df['LOCALIDADE'].nunique())
    c3.metric("Status", "Conectado", delta="OK")

    st.markdown("---")

    # GRÁFICO E TABELA
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        if 'LOCALIDADE' in df.columns:
            st.subheader("Filtros por Localidade")
            fig = px.bar(df['LOCALIDADE'].value_counts().reset_index(), 
                         x='index', y='LOCALIDADE', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Dados Recentes")
        st.dataframe(df.head(15), use_container_width=True)
else:
    st.warning("Verifique se a planilha está pública para 'Qualquer pessoa com o link'.")
