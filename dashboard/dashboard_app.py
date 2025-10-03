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
def load_data():
    try:
        caminhos = [
            '../dados_finais_ml.csv',
            'dados_finais_ml.csv',
        ]
        
        for caminho in caminhos:
            if os.path.exists(caminho):
                df = pd.read_csv(caminho)
                # Converter timestamp para datetime
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
    st.success(f"✅ Dados carregados com sucesso! {len(df)} registros encontrados.")
    
    # KPIs PRINCIPAIS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_leituras = len(df)
        st.metric('Total de Leituras', f'{total_leituras:,}')

    with col2:
        criticos = len(df[df['estado_alerta'] == 'CRITICO'])
        st.metric('Alertas Críticos', criticos, delta=f"{criticos/total_leituras*100:.1f}%")

    with col3:
        alertas = len(df[df['estado_alerta'] == 'ALERTA'])
        st.metric('Alertas de Atenção', alertas, delta=f"{alertas/total_leituras*100:.1f}%")

    with col4:
        anomalias = len(df[df['anomalia'] == -1])
        st.metric('Anomalias Detectadas', anomalias, delta=f"{anomalias/total_leituras*100:.1f}%")

    # GRÁFICOS PRINCIPAIS
    tab1, tab2, tab3, tab4 = st.tabs(['📈 Monitoramento Tempo Real', '🔍 Análise de Sensores', '🚨 Alertas & Anomalias', '📊 Clusters'])

    with tab1:
        st.subheader("Monitoramento em Tempo Real dos Sensores")
        
        # Gráfico de temperatura
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig_temp = px.line(df, x='timestamp', y='temperatura', 
                             title='Temperatura ao Longo do Tempo',
                             color_discrete_sequence=['#FF6B6B'])
            fig_temp.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Limite Crítico")
            fig_temp.update_layout(height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
        
        # Gráficos de vibração e distância
        col1_sens, col2_sens = st.columns(2)
        
        with col1_sens:
            if 'timestamp' in df.columns and 'vibracao' in df.columns:
                fig_vib = px.line(df, x='timestamp', y='vibracao', 
                                title='Vibração ao Longo do Tempo',
                                color_discrete_sequence=['#4ECDC4'])
                fig_vib.update_layout(height=300)
                st.plotly_chart(fig_vib, use_container_width=True)
        
        with col2_sens:
            if 'timestamp' in df.columns and 'distancia' in df.columns:
                fig_dist = px.line(df, x='timestamp', y='distancia', 
                                 title='Distância ao Longo do Tempo',
                                 color_discrete_sequence=['#45B7D1'])
                fig_dist.update_layout(height=300)
                st.plotly_chart(fig_dist, use_container_width=True)

    with tab2:
        st.subheader("Análise de Correlação entre Sensores")
        
        col1_anal, col2_anal = st.columns(2)
        
        with col1_anal:
            # Temperatura vs Vibração
            if all(col in df.columns for col in ['temperatura', 'vibracao']):
                fig_scatter = px.scatter(df, x='temperatura', y='vibracao',
                                       color='estado_alerta',
                                       title='Temperatura vs Vibração (Colorido por Alerta)',
                                       color_discrete_map={'NORMAL': 'green', 'ALERTA': 'orange', 'CRITICO': 'red'})
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2_anal:
            # Médias móveis
            if all(col in df.columns for col in ['timestamp', 'temperatura_media_movel']):
                fig_media = px.line(df, x='timestamp', y=['temperatura', 'temperatura_media_movel'],
                                  title='Temperatura vs Média Móvel',
                                  color_discrete_sequence=['#FF6B6B', '#1f77b4'])
                fig_media.update_layout(height=400)
                st.plotly_chart(fig_media, use_container_width=True)

    with tab3:
        st.subheader("Dashboard de Alertas e Anomalias")
        
        col1_alert, col2_alert = st.columns(2)
        
        with col1_alert:
            # Distribuição de alertas
            if 'estado_alerta' in df.columns:
                alert_counts = df['estado_alerta'].value_counts()
                fig_alerts = px.pie(values=alert_counts.values, names=alert_counts.index,
                                  title='Distribuição de Estados de Alerta',
                                  color=alert_counts.index,
                                  color_discrete_map={'NORMAL': 'green', 'ALERTA': 'orange', 'CRITICO': 'red'})
                st.plotly_chart(fig_alerts, use_container_width=True)
        
        with col2_alert:
            # Scores de anomalia
            if 'anomalia_score' in df.columns and 'timestamp' in df.columns:
                fig_anom = px.scatter(df, x='timestamp', y='anomalia_score',
                                    color='status_anomalia',
                                    title='Scores de Anomalia ao Longo do Tempo',
                                    color_discrete_map={'Normal': 'blue', 'Anomalia': 'red'})
                st.plotly_chart(fig_anom, use_container_width=True)
        
        # Tabela de alertas críticos
        st.subheader("Registros com Alertas Críticos")
        criticos_df = df[df['estado_alerta'] == 'CRITICO']
        if not criticos_df.empty:
            st.dataframe(criticos_df[['timestamp', 'temperatura', 'vibracao', 'distancia', 'anomalia_score']].sort_values('temperatura', ascending=False))
        else:
            st.info("✅ Nenhum alerta crítico detectado")

    with tab4:
        st.subheader("Análise de Clusters")
        
        if 'cluster' in df.columns:
            col1_clust, col2_clust = st.columns(2)
            
            with col1_clust:
                # Distribuição de clusters
                cluster_counts = df['cluster'].value_counts().sort_index()
                fig_cluster = px.bar(x=cluster_counts.index, y=cluster_counts.values,
                                   title='Distribuição de Clusters',
                                   labels={'x': 'Cluster', 'y': 'Quantidade'})
                st.plotly_chart(fig_cluster, use_container_width=True)
            
            with col2_clust:
                # Clusters vs Temperatura
                fig_cluster_temp = px.box(df, x='cluster', y='temperatura',
                                        title='Temperatura por Cluster')
                st.plotly_chart(fig_cluster_temp, use_container_width=True)

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.subheader("📋 Resumo Executivo")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.write("**🔴 Situação Crítica:**")
        st.write(f"- {criticos} registros em estado CRÍTICO")
        st.write(f"- Temperatura máxima: {df['temperatura'].max():.1f}°C")
    
    with col_res2:
        st.write("**🟠 Alertas:**")
        st.write(f"- {alertas} registros requerem atenção")
        st.write(f"- {anomalias} anomalias detectadas")
    
    with col_res3:
        st.write("**📊 Estatísticas:**")
        st.write(f"- Temperatura média: {df['temperatura'].mean():.1f}°C")
        st.write(f"- Vibração média: {df['vibracao'].mean():.2f}")
        st.write(f"- Período: {df['timestamp'].min().strftime('%d/%m %H:%M')} a {df['timestamp'].max().strftime('%d/%m %H:%M')}")

else:
    st.error('''
    ⚠️ **Sistema não inicializado**

    Para usar o dashboard:

    1. **Execute o pipeline de Machine Learning**  
    2. **Certifique-se que 'dados_finais_ml.csv' existe na pasta raiz**  
    3. **Ou faça upload do arquivo na sidebar**  
    4. **Recarregue esta página**  
    ''')

# Rodapé
st.markdown('---')
st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')
