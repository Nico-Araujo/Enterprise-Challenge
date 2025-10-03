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
    
# MÉTODO 3: Criando DataFrame explícito
    st.subheader("Método 3: DataFrame explícito")
    
    df_pizza = pd.DataFrame({
        'estado': ['NORMAL', 'ALERTA', 'CRITICO'],
        'quantidade': [normal_count, alerta_count, critico_count]
    })
    st.write("**DataFrame para pizza:**")
    st.dataframe(df_pizza)
    
    # Gráfico 3: Usando DataFrame
    st.subheader("Gráfico 3: Com DataFrame")
    try:
        fig3 = px.pie(
            df_pizza,
            values='quantidade',
            names='estado',
            title='Distribuição de Alertas (DataFrame)'
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.success("✅ Gráfico 3 criado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro Gráfico 3: {e}")
    
    # DEBUG: Informações extras
    st.subheader("🔍 Debug Info")
    st.write(f"Valores únicos em estado_alerta: {df['estado_alerta'].unique()}")
    st.write(f"Tipos de dados: {df['estado_alerta'].dtype}")
    st.write("Amostra de dados:")
    st.dataframe(df[['estado_alerta']].head(10))

else:
    st.error('⚠️ Dados não carregados ou coluna estado_alerta não encontrada')
