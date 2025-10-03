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
    
    # MÉTODO 3: Criando DataFrame explícito - CORRIGIDO
    st.subheader("Método 3: DataFrame explícito")
    
    # CORREÇÃO: Criar o DataFrame corretamente
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
    
    # MÉTODO 4: Versão mais simples
    st.subheader("Método 4: Versão Simplificada")
    
    # Apenas criar o gráfico diretamente sem variáveis intermediárias
    try:
        fig4 = px.pie(
            values=[normal_count, alerta_count, critico_count],
            names=['NORMAL', 'ALERTA', 'CRITICO'],
            title='Distribuição de Alertas (Simplificado)'
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.success("✅ Gráfico 4 criado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro Gráfico 4: {e}")
    
    # DEBUG: Informações extras
    st.subheader("🔍 Debug Info")
    st.write(f"Valores únicos em estado_alerta: {list(df['estado_alerta'].unique())}")
    st.write(f"Tipos de dados: {df['estado_alerta'].dtype}")
    st.write("Amostra de dados:")
    st.dataframe(df[['estado_alerta']].head(10))

else:
    if df.empty:
        st.error('⚠️ Dados não carregados')
    else:
        st.error('⚠️ Coluna estado_alerta não encontrada')
    st.write("Colunas disponíveis:", list(df.columns) if not df.empty else "Nenhuma")
