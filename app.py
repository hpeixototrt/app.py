import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de página "Dashboard Premium"
st.set_page_config(page_title="Controle de Filtros TRT", layout="wide")

# CSS para dar cara de infográfico (Cards coloridos)
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
    }
    [data-testid="stMetricValue"] { color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

SHEET_ID = "1XQi3Z4BbYqu9OvZFGsR_gBZo2N68C5KFGMrt4HL-Cok"
# Note o 'skip=1' ou similar se sua planilha tiver lixo no topo. 
# Aqui vamos limpar via Pandas para ser mais seguro.
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1429723031"

def load_data():
    df = pd.read_csv(CSV_URL)
    # Remove colunas e linhas totalmente vazias que o Sheets costuma mandar
    df = df.dropna(how='all').dropna(axis=1, how='all')
    return df

df = load_data()

if df is not None:
    st.title("🚰 Painel Estratégico de Filtros - TRT21")
    
    # --- LINHA 1: CARDS DE IMPACTO ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Supondo que a coluna com os nomes das marcas seja a primeira ou tenha um nome específico
    # Vamos usar a contagem real de linhas para o total
    total_filtros = len(df)
    
    col1.metric("Total de Equipamentos", f"{total_filtros} Unid.")
    col2.metric("Marcas Atendidas", df.shape[1]) # Número de colunas/marcas
    col3.metric("Status da Rede", "Operacional", delta="100%")
    col4.metric("Sincronização", "Tempo Real")

    st.markdown("---")

    # --- LINHA 2: GRÁFICOS INTERATIVOS ---
    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("📊 Volume por Fabricante/Modelo")
        # Transformando a linha de totais da sua planilha em um gráfico de barras
        if not df.empty:
            # Pegamos a primeira linha que parece conter os totais no seu print
            dados_grafico = df.iloc[0].to_frame().reset_index()
            dados_grafico.columns = ['Modelo', 'Quantidade']
            # Limpeza rápida para o gráfico não bugar
            dados_grafico = dados_grafico[dados_grafico['Quantidade'].apply(lambda x: str(x).replace(' UNIDADES', '').isdigit() if pd.notnull(x) else False)]
            
            fig = px.bar(dados_grafico, x='Modelo', y='Quantidade', 
                         text_auto=True, color='Quantidade',
                         color_continuous_scale='Blues', template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("📈 Percentual de Frota")
        fig_pie = px.pie(dados_grafico, names='Modelo', values='Quantidade', 
                         hole=.4, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- LINHA 3: TABELA LIMPA ---
    st.subheader("📑 Detalhamento Técnico")
    st.dataframe(df, use_container_width=True)

else:
    st.error("Não foi possível carregar os dados. Verifique a permissão da planilha.")
