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
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total de Leituras', len(df))
    with col2:
        criticos = len(df[df['estado_alerta'] == 'CRITICO'])
        st.metric('Alertas Críticos', criticos)
    with col3:
        alertas = len(df[df['estado_alerta'] == 'ALERTA'])
        st.metric('Alertas de Atenção', alertas)
    with col4:
        anomalias = len(df[df['anomalia'] == -1])
        st.metric('Anomalias', anomalias)

    # GRÁFICOS CORRIGIDOS
    tab1, tab2, tab3, tab4 = st.tabs(['📈 Tempo Real', '🔍 Sensores', '🚨 Alertas', '📊 Clusters'])

    with tab1:
        st.subheader("Monitoramento em Tempo Real")
        
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig_temp = px.line(df, x='timestamp', y='temperatura', 
                             title='Temperatura ao Longo do Tempo',
                             labels={'temperatura': 'Temperatura (°C)', 'timestamp': 'Tempo'})
            st.plotly_chart(fig_temp, use_container_width=True)
        
        col1_sens, col2_sens = st.columns(2)
        with col1_sens:
            if 'timestamp' in df.columns and 'vibracao' in df.columns:
                fig_vib = px.line(df, x='timestamp', y='vibracao', 
                                title='Vibração ao Longo do Tempo',
                                labels={'vibracao': 'Vibração', 'timestamp': 'Tempo'})
                st.plotly_chart(fig_vib, use_container_width=True)
        with col2_sens:
            if 'timestamp' in df.columns and 'distancia' in df.columns:
                fig_dist = px.line(df, x='timestamp', y='distancia', 
                                 title='Distância ao Longo do Tempo',
                                 labels={'distancia': 'Distância', 'timestamp': 'Tempo'})
                st.plotly_chart(fig_dist, use_container_width=True)

    with tab2:
        st.subheader("Análise de Sensores")
        
        # GRÁFICO 1: Temperatura vs Vibração - CORRIGIDO
        if all(col in df.columns for col in ['temperatura', 'vibracao', 'estado_alerta']):
            # Verificar os valores reais
            st.write(f"📊 Estatísticas reais:")
            st.write(f"- Temperatura: {df['temperatura'].min():.1f}°C a {df['temperatura'].max():.1f}°C")
            st.write(f"- Vibração: {df['vibracao'].min():.2f} a {df['vibracao'].max():.2f}")
            
            # Criar scatter plot com dados reais
            fig_scatter = px.scatter(
                df,
                x='temperatura',
                y='vibracao', 
                color='estado_alerta',
                title='Temperatura vs Vibração (Dados Reais)',
                labels={
                    'temperatura': 'Temperatura (°C)', 
                    'vibracao': 'Vibração',
                    'estado_alerta': 'Estado de Alerta'
                },
                color_discrete_map={
                    'NORMAL': 'green', 
                    'ALERTA': 'orange', 
                    'CRITICO': 'red'
                }
            )
            # Ajustar os eixos para mostrar os dados reais
            fig_scatter.update_xaxes(range=[df['temperatura'].min()-5, df['temperatura'].max()+5])
            fig_scatter.update_yaxes(range=[df['vibracao'].min()-0.5, df['vibracao'].max()+0.5])
            st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        st.subheader("Alertas e Anomalias")
        
        # GRÁFICO 2: Pizza de alertas - CORRIGIDO
        if 'estado_alerta' in df.columns:
            # Criar DataFrame para o gráfico de pizza
            alert_data = df['estado_alerta'].value_counts().reset_index()
            alert_data.columns = ['estado', 'quantidade']
            
            fig_pizza = px.pie(
                alert_data,
                values='quantidade',
                names='estado',
                title='Distribuição Real de Estados de Alerta',
                color='estado',
                color_discrete_map={
                    'NORMAL': 'green', 
                    'ALERTA': 'orange', 
                    'CRITICO': 'red'
                }
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
            
            # Mostrar os valores reais
            st.write("**Valores reais:**")
            for estado, quantidade in alert_data.values:
                st.write(f"- {estado}: {quantidade} registros ({quantidade/len(df)*100:.1f}%)")

    with tab4:
        st.subheader("Análise de Clusters")
        
        if 'cluster' in df.columns:
            # Converter cluster para string para funcionar como categoria
            df['cluster_str'] = df['cluster'].astype(str)
            
            col1_clust, col2_clust = st.columns(2)
            
            with col1_clust:
                # Distribuição de clusters - CORRIGIDO
                cluster_counts = df['cluster_str'].value_counts().sort_index()
                
                fig_barras = px.bar(
                    x=cluster_counts.index,
                    y=cluster_counts.values,
                    title='Distribuição Real de Clusters',
                    labels={'x': 'Cluster', 'y': 'Quantidade de Registros'},
                    color=cluster_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_barras, use_container_width=True)
                
                # Mostrar valores reais
                st.write("**Contagem por cluster:**")
                for cluster, count in cluster_counts.items():
                    st.write(f"- Cluster {cluster}: {count} registros")
            
            with col2_clust:
                # Box plot de temperatura por cluster
                fig_box = px.box(
                    df,
                    x='cluster_str',
                    y='temperatura',
                    title='Temperatura por Cluster',
                    color='cluster_str',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig_box, use_container_width=True)

            # Scatter plot clusters
            st.subheader("Relação entre Sensores por Cluster")
            fig_cluster_scatter = px.scatter(
                df,
                x='temperatura',
                y='vibracao',
                color='cluster_str',
                title='Clusters: Temperatura vs Vibração',
                labels={
                    'temperatura': 'Temperatura (°C)',
                    'vibracao': 'Vibração',
                    'cluster_str': 'Cluster'
                },
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_cluster_scatter, use_container_width=True)

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.subheader("📋 Resumo Executivo")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.write("**🔴 Situação Crítica:**")
        st.write(f"- {criticos} registros em estado CRÍTICO")
        st.write(f"- Temperatura máxima: {df['temperatura'].max():.1f}°C")
        if 'cluster' in df.columns:
            cluster_critico = df[df['estado_alerta'] == 'CRITICO']['cluster'].value_counts().index[0]
            st.write(f"- Cluster com mais críticos: {cluster_critico}")
    
    with col_res2:
        st.write("**🟠 Alertas:**")
        st.write(f"- {alertas} registros requerem atenção")
        st.write(f"- {anomalias} anomalias detectadas")
        st.write(f"- Período analisado: {len(df)} leituras")
    
    with col_res3:
        st.write("**📊 Estatísticas:**")
        st.write(f"- Temperatura média: {df['temperatura'].mean():.1f}°C")
        st.write(f"- Vibração média: {df['vibracao'].mean():.2f}")
        st.write(f"- Distância média: {df['distancia'].mean():.1f}")

else:
    st.error('⚠️ Sistema não inicializado')

st.markdown('---')
st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')
