import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import joblib
import json
import os

# Configuração da página
st.set_page_config(
    page_title='Monitoramento Inteligente - Hermes Reply',
    page_icon='🚀',
    layout='wide'
)

# CSS personalizado
st.markdown('''
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
''', unsafe_allow_html=True)

# Cabeçalho
st.markdown('<h1 class="main-header">🚀 Monitoramento Inteligente - Hermes Reply</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title('⚙️ Controles')
uploaded_file = st.sidebar.file_uploader('Carregar dados', type=['csv'])

# Carregar dados
@st.cache_data
def load_data(uploaded_file):
    try:
        # Check if the file exists in the current directory first
        if os.path.exists('dados_finais_ml.csv'):
            df = pd.read_csv('dados_finais_ml.csv')
            st.sidebar.success('Dados carregados do arquivo local.')
            return df
        elif uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success('Dados carregados do arquivo uploaded.')
            return df
        else:
            st.sidebar.warning('Por favor, carregue um arquivo CSV.')
            return pd.DataFrame()

    except Exception as e:
        st.sidebar.error(f'Erro ao carregar dados: {e}')
        return pd.DataFrame()

# Carregar modelos (using st.cache_resource)
@st.cache_resource
def load_models():
    models = {}
    try:
        if os.path.exists('models/isolation_forest.pkl'):
            models['isolation_forest'] = joblib.load('models/isolation_forest.pkl')
            st.sidebar.success('Isolation Forest carregado.')
        if os.path.exists('models/random_forest_classifier.pkl'):
            models['random_forest'] = joblib.load('models/random_forest_classifier.pkl')
            st.sidebar.success('Random Forest carregado.')
        if os.path.exists('models/kmeans_cluster.pkl'):
            models['kmeans'] = joblib.load('models/kmeans_cluster.pkl')
            st.sidebar.success('KMeans carregado.')
        if os.path.exists('models/ml_results.json'):
            with open('models/ml_results.json', 'r') as f:
                models['results'] = json.load(f)
                st.sidebar.success('Resultados de ML carregados.')
        st.sidebar.info(f'Total de modelos carregados: {len(models)}')
        return models
    except Exception as e:
        st.sidebar.error(f'Erro ao carregar modelos: {e}')
        return {}


df = load_data(uploaded_file)
models = load_models()
if not df.empty:
    # Convert 'data_hora_ms' to datetime if it exists
    if 'data_hora_ms' in df.columns:
        df['data_hora'] = pd.to_datetime(df['data_hora_ms'], unit='ms')

    # KPIs
    st.subheader('📊 KPIs Principais')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Leituras', f'{len(df):,}')

    with col2:
        criticos = len(df[df.get('estado_alerta', '') == 'CRITICO']) if 'estado_alerta' in df.columns else 0
        st.metric('Alertas Críticos', criticos)

    with col3:
        atencao = len(df[df.get('estado_alerta', '') == 'ALERTA']) if 'estado_alerta' in df.columns else 0
        st.metric('Alertas de Atenção', atencao)

    with col4:
        anomalias = (df['anomalia'] == -1).sum() if 'anomalia' in df.columns else 0
        st.metric('Anomalias', anomalias)

    # Gráficos
    st.subheader('📈 Visualizações')
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['📈 Série Temporal (Temperatura)', '📊 Série Temporal (Vibração)', '📏 Série Temporal (Distância)', '🔍 Análise Dispersão', '🚨 Distribuição de Alertas'])

    with tab1:
        if 'temperatura' in df.columns and 'data_hora' in df.columns:
            fig_temp = px.line(df, x='data_hora', y='temperatura',
                             title='Temperatura ao Longo do Tempo')
            st.plotly_chart(fig_temp, use_container_width=True)
        else:
            st.warning('Dados de temperatura ou timestamp não disponíveis para série temporal.')

    with tab2:
        if 'vibracao' in df.columns and 'data_hora' in df.columns:
            fig_vib = px.line(df, x='data_hora', y='vibracao',
                             title='Vibração ao Longo do Tempo')
            st.plotly_chart(fig_vib, use_container_width=True)
        else:
            st.warning('Dados de vibração ou timestamp não disponíveis para série temporal.')

    with tab3:
        if 'distancia' in df.columns and 'data_hora' in df.columns:
            fig_dist = px.line(df, x='data_hora', y='distancia',
                             title='Distância ao Longo do Tempo')
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.warning('Dados de distância ou timestamp não disponíveis para série temporal.')

    with tab4:
        if all(col in df.columns for col in ['temperatura', 'vibracao']):
            fig_scatter = px.scatter(df, x='temperatura', y='vibracao',
                                   color='estado_alerta' if 'estado_alerta' in df.columns else None,
                                   title='Relação Temperatura vs Vibração')
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
             st.warning('Dados de temperatura ou vibração não disponíveis para análise de dispersão.')

    with tab5:
        if 'estado_alerta' in df.columns:
            alert_counts = df['estado_alerta'].value_counts()
            fig_alerts = px.pie(values=alert_counts.values, names=alert_counts.index,
                              title='Distribuição de Alertas')
            st.plotly_chart(fig_alerts, use_container_width=True)
        else:
            st.warning('Dados de alerta não disponíveis para distribuição.')
    # Machine Learning Insights (if models loaded)
    if models:
        st.subheader('🤖 Machine Learning Insights')
        if 'results' in models and models['results']:
            ml_results = models['results']
            st.write('**Resultados do Modelo:**')
            st.json(ml_results)
        if 'anomalia' in df.columns:
            st.write('**Anomalias Detectadas Recentemente:**')
            anomaly_alerts = df[df['anomalia'] == -1].tail(10)
            if not anomaly_alerts.empty:
                st.dataframe(anomaly_alerts)
            else:
                st.info('Nenhuma anomalia recente detectada.')
        if 'cluster' in df.columns:
            st.write('**Distribuição de Clusters:**')
            cluster_counts = df['cluster'].value_counts().sort_index()
            fig_clusters = px.bar(x=[f'Cluster {i}' for i in cluster_counts.index], y=cluster_counts.values, title='Distribuição dos Clusters')
            st.plotly_chart(fig_clusters, use_container_width=True)
else:
    st.warning('''
⚠️ **Sistema não inicializado**

Para usar o dashboard:
1. Execute o pipeline de Machine Learning
2. Certifique-se que 'dados_finais_ml.csv' existe na pasta raiz ou faça upload
3. Recarregue esta página
''')

# Rodapé
st.markdown('---')
st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')
