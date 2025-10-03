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
    
   # MÉTODO 2: Usando value_counts()
    st.subheader("Método 2: value_counts()")
    
    contagens = df['estado_alerta'].value_counts()
    st.write("**value_counts():**")
    st.write(contagens)
    
    # Gráfico 2: Usando value_counts diretamente
    st.subheader("Gráfico 2: value_counts direto")
    try:
        fig2 = px.pie(
            values=contagens.values,
            names=contagens.index,
            title='Distribuição de Alertas (value_counts)'
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.success("✅ Gráfico 2 criado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro Gráfico 2: {e}")
    
    
