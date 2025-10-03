import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title='Teste Gráfico Pizza', layout='wide')
st.title('🧪 Teste - Gráfico de Pizza de Alertas')

# Carregar dados
@st.cache_data
def load_data():
    try:
        caminhos = ['../dados_finais_ml.csv', 'dados_finais_ml.csv']
        for caminho in caminhos:
            if os.path.exists(caminho):
                df = pd.read_csv(caminho)
                return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f'Erro: {e}')
        return pd.DataFrame()

df = load_data()

if not df.empty and 'estado_alerta' in df.columns:
    st.success(f"✅ Dados carregados: {len(df)} registros")
    
    # MÉTODO 1: Contagem manual explícita
    st.subheader("Método 1: Contagem Manual")
    
    normal_count = len(df[df['estado_alerta'] == 'NORMAL'])
    alerta_count = len(df[df['estado_alerta'] == 'ALERTA'])
    critico_count = len(df[df['estado_alerta'] == 'CRITICO'])
    
    st.write(f"**Contagens manuais:**")
    st.write(f"- NORMAL: {normal_count}")
    st.write(f"- ALERTA: {alerta_count}") 
    st.write(f"- CRITICO: {critico_count}")
    st.write(f"- Total: {normal_count + alerta_count + critico_count}")
    
    # Criar arrays separados para valores e nomes
    valores = [normal_count, alerta_count, critico_count]
    nomes = ['NORMAL', 'ALERTA', 'CRITICO']
    
    # Gráfico 1: Usando arrays separados
    st.subheader("Gráfico 1: Arrays separados")
    try:
        fig1 = px.pie(
            values=valores,
            names=nomes,
            title='Distribuição de Alertas (Arrays)'
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.success("✅ Gráfico 1 criado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro Gráfico 1: {e}")
    
    
