import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title='Monitoramento Inteligente - Hermes Reply',
    page_icon='🚀',
    layout='wide'
)

st.title('🚀 Monitoramento Inteligente - Hermes Reply')

# Sidebar
st.sidebar.title('⚙️ Controles')
uploaded_file = st.sidebar.file_uploader('Carregar dados', type=['csv'])

# Carregar dados
@st.cache_data
def load_data():
    try:
        caminhos = [
            '../dados_finais_ml.csv',
            'dados_finais_ml.csv',
        ]
        
        for caminho in caminhos:
            if os.path.exists(caminho):
                df = pd.read_csv(caminho)
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        
        return pd.DataFrame()

    except Exception as e:
        st.error(f'Erro ao carregar dados: {str(e)}')
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.success(f"✅ Dados carregados: {len(df)} registros")
    
    # DEBUG: Mostrar informações dos dados problemáticos
    st.sidebar.subheader("🔍 Debug Info")
    
    # Informações sobre estado_alerta
    if 'estado_alerta' in df.columns:
        alert_counts = df['estado_alerta'].value_counts()
        st.sidebar.write("**Contagem de Alertas:**")
        for estado, count in alert_counts.items():
            st.sidebar.write(f"- {estado}: {count}")
        
        # Verificar valores únicos
        st.sidebar.write(f"Valores únicos em estado_alerta: {df['estado_alerta'].unique()}")
    
    # Informações sobre clusters
    if 'cluster' in df.columns:
        st.sidebar.write(f"Valores únicos em cluster: {df['cluster'].unique()}")
        st.sidebar.write(f"Contagem de clusters: {df['cluster'].value_counts().to_dict()}")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total de Leituras', len(df))
    with col2:
        criticos = len(df[df['estado_alerta'] == 'CRITICO']) if 'estado_alerta' in df.columns else 0
        st.metric('Alertas Críticos', criticos)
    with col3:
        alertas = len(df[df['estado_alerta'] == 'ALERTA']) if 'estado_alerta' in df.columns else 0
        st.metric('Alertas de Atenção', alertas)
    with col4:
        anomalias = len(df[df['anomalia'] == -1]) if 'anomalia' in df.columns else 0
        st.metric('Anomalias', anomalias)

    # GRÁFICOS COM DEBUG
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['📈 Tempo Real', '🔍 Sensores', '🚨 Alertas', '📊 Clusters', '🐛 Debug'])

    with tab1:
        st.subheader("Monitoramento em Tempo Real")
        
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig_temp = px.line(df, x='timestamp', y='temperatura', title='Temperatura')
            st.plotly_chart(fig_temp, use_container_width=True)

    with tab2:
        st.subheader("Análise de Sensores")
        
        # GRÁFICO 1: Temperatura vs Vibração - VERSÃO SIMPLIFICADA
        if all(col in df.columns for col in ['temperatura', 'vibracao', 'estado_alerta']):
            st.write("**Dados para scatter plot:**")
            st.write(f"- Temperatura: {df['temperatura'].notna().sum()} valores válidos")
            st.write(f"- Vibração: {df['vibracao'].notna().sum()} valores válidos")
            st.write(f"- Estados de alerta: {df['estado_alerta'].notna().sum()} valores válidos")
            
            # Criar uma versão simplificada do scatter plot
            try:
                fig = px.scatter(
                    df,
                    x='temperatura',
                    y='vibracao', 
                    color='estado_alerta',
                    title='Temperatura vs Vibração'
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro no scatter plot: {e}")
                
                # Tentar versão alternativa sem cores
                try:
                    fig = px.scatter(df, x='temperatura', y='vibracao', title='Temperatura vs Vibração (sem cores)')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e2:
                    st.error(f"Erro mesmo sem cores: {e2}")

    with tab3:
        st.subheader("Alertas e Anomalias")
        
        # GRÁFICO 2: Pizza de alertas - VERSÃO SIMPLIFICADA
        if 'estado_alerta' in df.columns:
            st.write("**Dados para gráfico de pizza:**")
            
            # Método 1: Usando value_counts diretamente
            alert_counts = df['estado_alerta'].value_counts()
            st.write("Contagem por value_counts:", alert_counts.to_dict())
            
            # Método 2: Contagem manual
            normal_count = len(df[df['estado_alerta'] == 'NORMAL'])
            alerta_count = len(df[df['estado_alerta'] == 'ALERTA']) 
            critico_count = len(df[df['estado_alerta'] == 'CRITICO'])
            st.write(f"Contagem manual - NORMAL: {normal_count}, ALERTA: {alerta_count}, CRITICO: {critico_count}")
            
            # Tentar criar o gráfico de pizza
            if len(alert_counts) > 0:
                try:
                    fig = px.pie(
                        values=alert_counts.values,
                        names=alert_counts.index,
                        title='Distribuição de Alertas'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro no gráfico de pizza: {e}")

    with tab4:
        st.subheader("Análise de Clusters")
        
        if 'cluster' in df.columns:
            st.write("**Dados para gráficos de cluster:**")
            st.write(f"Clusters únicos: {df['cluster'].unique()}")
            st.write(f"Contagem: {df['cluster'].value_counts().to_dict()}")
            
            # GRÁFICO 3: Distribuição de clusters - VERSÃO SIMPLIFICADA
            cluster_counts = df['cluster'].value_counts().sort_index()
            
            # Método 1: Gráfico de barras simples
            try:
                fig = px.bar(
                    x=cluster_counts.index.astype(str),
                    y=cluster_counts.values,
                    title='Distribuição de Clusters',
                    labels={'x': 'Cluster', 'y': 'Quantidade'}
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro no gráfico de barras: {e}")

    with tab5:
        st.subheader("Debug Completo")
        
        st.write("**DataFrame completo:**")
        st.dataframe(df)
        
        st.write("**Info do DataFrame:**")
        st.write(f"Colunas: {list(df.columns)}")
        st.write(f"Tipos de dados: {df.dtypes.to_dict()}")
        
        if 'estado_alerta' in df.columns:
            st.write("**Amostra de estado_alerta:**")
            st.write(df[['timestamp', 'temperatura', 'estado_alerta']].head(10))
        
        if 'cluster' in df.columns:
            st.write("**Amostra de cluster:**")
            st.write(df[['timestamp', 'temperatura', 'cluster']].head(10))

else:
    st.error('⚠️ Sistema não inicializado')

st.markdown('---')
st.markdown('**Hermes Reply - Fase 4**')
