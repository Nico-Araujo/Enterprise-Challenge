import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# --- CONFIGURAÇÕES E ESTILOS GLOBAIS ---

# Definição de Cores para Alertas (Para consistência em todos os gráficos)
ALERTA_COLOR_MAP = {
    'NORMAL': 'green',
    'ALERTA': 'orange',
    'CRITICO': 'red'
}

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

# Sidebar e Upload de Arquivo
st.sidebar.title('⚙️ Controles')
uploaded_file = st.sidebar.file_uploader('Carregar dados', type=['csv'])

# --- FUNÇÃO DE CARREGAMENTO DE DADOS OTIMIZADA ---

# A função agora recebe o uploaded_file e prioriza o arquivo do usuário, 
# só então buscando os arquivos locais.
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.DataFrame()
        
        # 1. Tentar carregar arquivo enviado pelo usuário
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ Dados carregados via Upload.")
        
        # 2. Se não houver upload, tentar caminhos fixos (fallback)
        if df.empty:
            caminhos = [
                'dados_finais_ml.csv',  # Pasta atual
                '../dados_finais_ml.csv', # Um nível acima
            ]
            
            for caminho in caminhos:
                if os.path.exists(caminho):
                    df = pd.read_csv(caminho)
                    st.sidebar.info(f"💾 Dados carregados de: {caminho}")
                    break
        
        # 3. Se o DataFrame foi carregado, fazer conversões
        if not df.empty and 'timestamp' in df.columns:
            # Converter timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Adicionar coluna auxiliar para clusters, se existir
            if 'cluster' in df.columns:
                df['cluster_str'] = df['cluster'].astype(str)
                
        return df

    except Exception as e:
        st.error(f'❌ Erro ao carregar dados. Verifique o formato do CSV: {str(e)}')
        return pd.DataFrame()

df = load_data(uploaded_file)

# --- INÍCIO DO DASHBOARD ---

if not df.empty:
    st.success(f"✅ Dados carregados com sucesso! **{len(df):,.0f}** registros encontrados.")
    
    # Adicionando um fallback se colunas críticas estiverem faltando
    COLUNAS_CRITICAS = ['temperatura', 'vibracao', 'distancia', 'estado_alerta', 'timestamp']
    if not all(col in df.columns for col in COLUNAS_CRITICAS):
        st.error("⚠️ **Erro de Estrutura:** O CSV carregado está faltando colunas críticas ('temperatura', 'vibracao', 'estado_alerta', etc.).")
        st.stop()
        
    # KPIs PRINCIPAIS
    col1, col2, col3, col4 = st.columns(4)
    total_leituras = len(df)
    
    # Correção: Formatação de números grandes nos KPIs
    with col1:
        st.metric('Total de Leituras', f'{total_leituras:,.0f}'.replace(',', '.'))

    with col2:
        criticos = len(df[df['estado_alerta'] == 'CRITICO'])
        # Tratamento para evitar divisão por zero se o df estiver vazio
        delta_criticos = f"{criticos/total_leituras*100:.1f}%" if total_leituras > 0 else "0.0%"
        st.metric('Alertas Críticos', f'{criticos:,.0f}'.replace(',', '.'), delta=delta_criticos)

    with col3:
        alertas = len(df[df['estado_alerta'] == 'ALERTA'])
        delta_alertas = f"{alertas/total_leituras*100:.1f}%" if total_leituras > 0 else "0.0%"
        st.metric('Alertas de Atenção', f'{alertas:,.0f}'.replace(',', '.'), delta=delta_alertas)

    with col4:
        # Coluna 'anomalia' pode não existir se o modelo não rodou
        anomalias = len(df[df['anomalia'] == -1]) if 'anomalia' in df.columns else 0
        delta_anomalias = f"{anomalias/total_leituras*100:.1f}%" if total_leituras > 0 else "0.0%"
        st.metric('Anomalias Detectadas', f'{anomalias:,.0f}'.replace(',', '.'), delta=delta_anomalias)

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
            # Gráfico de Dispersão (Temperatura vs Vibração)
            if all(col in df.columns for col in ['temperatura', 'vibracao', 'estado_alerta']):
                # Verificar se há dados válidos (CORREÇÃO DE BUG: Garante que o gráfico não fique vazio por NaNs)
                df_valid = df.dropna(subset=['temperatura', 'vibracao'])
                
                if len(df_valid) > 0:
                    fig_scatter = px.scatter(
                        df_valid, 
                        x='temperatura', 
                        y='vibracao',
                        color='estado_alerta',
                        title='Temperatura vs Vibração (Colorido por Alerta)',
                        color_discrete_map=ALERTA_COLOR_MAP # Uso do mapa de cores consistente
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.warning("Dados insuficientes para o gráfico de dispersão: Muitos valores nulos em Temperatura/Vibração.")
        
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
            # Distribuição de alertas (Gráfico de Pizza)
            if 'estado_alerta' in df.columns:
                # Contagem de valores para garantir precisão e tratar estados ausentes
                alert_counts = df['estado_alerta'].value_counts()
                
                # Criar DataFrame para o gráfico, garantindo que o Plotly consiga plotar
                alert_df = pd.DataFrame({
                    'estado': alert_counts.index,
                    'quantidade': alert_counts.values
                })
                
                if not alert_df.empty:
                    fig_alerts = px.pie(
                        alert_df, 
                        values='quantidade', 
                        names='estado',
                        title='Distribuição de Estados de Alerta',
                        color='estado',
                        color_discrete_map=ALERTA_COLOR_MAP # Uso do mapa de cores consistente
                    )
                    st.plotly_chart(fig_alerts, use_container_width=True)
                else:
                    st.warning("Nenhum dado de alerta disponível. Verifique a coluna 'estado_alerta'.")
        
        with col2_alert:
            # Scores de anomalia
            if 'anomalia_score' in df.columns and 'timestamp' in df.columns and 'status_anomalia' in df.columns:
                fig_anom = px.scatter(df, x='timestamp', y='anomalia_score',
                                     color='status_anomalia',
                                     title='Scores de Anomalia ao Longo do Tempo',
                                     color_discrete_map={'Normal': 'blue', 'Anomalia': 'red'})
                st.plotly_chart(fig_anom, use_container_width=True)
            else:
                 st.info("Colunas 'anomalia_score' ou 'status_anomalia' não encontradas para o gráfico de anomalias.")
        
        # Tabela de alertas críticos
        st.subheader("Registros com Alertas Críticos")
        criticos_df = df[df['estado_alerta'] == 'CRITICO']
        colunas_tabela = ['timestamp', 'temperatura', 'vibracao', 'distancia']
        
        # Incluir 'anomalia_score' se existir
        if 'anomalia_score' in df.columns:
             colunas_tabela.append('anomalia_score')

        if not criticos_df.empty:
            st.dataframe(criticos_df[colunas_tabela].sort_values('temperatura', ascending=False))
        else:
            st.info("✅ Nenhum alerta crítico detectado")

    with tab4:
        st.subheader("Análise de Clusters")
        
        if 'cluster' in df.columns and 'cluster_str' in df.columns:
            
            col1_clust, col2_clust = st.columns(2)
            
            # Checagem de colunas para os gráficos de cluster
            if all(col in df.columns for col in ['temperatura', 'vibracao']):
                
                with col1_clust:
                    # Distribuição de clusters (CORREÇÃO DE BUG: Garante a plotagem correta)
                    cluster_counts = df['cluster_str'].value_counts().sort_index()
                    cluster_df = pd.DataFrame({
                        'cluster': cluster_counts.index,
                        'quantidade': cluster_counts.values
                    })
                    
                    fig_cluster_bar = px.bar(
                        cluster_df,
                        x='cluster', 
                        y='quantidade',
                        title='Distribuição de Clusters',
                        labels={'quantidade': 'Quantidade de Registros'},
                        color='cluster',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_cluster_bar.update_layout(showlegend=False)
                    st.plotly_chart(fig_cluster_bar, use_container_width=True)
                    
                    # Scatter plot clusters (CORREÇÃO DE BUG: Garante que não fique vazio por NaNs)
                    cluster_valid = df.dropna(subset=['temperatura', 'vibracao'])
                    
                    if len(cluster_valid) > 0:
                        fig_cluster_scatter = px.scatter(
                            cluster_valid, 
                            x='temperatura', 
                            y='vibracao',
                            color='cluster_str',
                            title='Clusters: Temperatura vs Vibração',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig_cluster_scatter, use_container_width=True)
                    else:
                        st.warning("Dados insuficientes para scatter plot de clusters.")
                
                with col2_clust:
                    # Box plot por cluster - Temperatura
                    fig_cluster_temp = px.box(
                        df, 
                        x='cluster_str', 
                        y='temperatura',
                        title='Distribuição de Temperatura por Cluster',
                        color='cluster_str',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_cluster_temp.update_layout(showlegend=False)
                    st.plotly_chart(fig_cluster_temp, use_container_width=True)
                    
                    # Box plot vibração por cluster
                    fig_cluster_vib = px.box(
                        df, 
                        x='cluster_str', 
                        y='vibracao',
                        title='Distribuição de Vibração por Cluster',
                        color='cluster_str',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_cluster_vib.update_layout(showlegend=False)
                    st.plotly_chart(fig_cluster_vib, use_container_width=True)
                
                # Análise dos clusters
                st.subheader("Características dos Clusters")
                
                # Adicionando uma coluna 'Alertas Críticos' baseada na contagem para o resumo
                cluster_stats = df.groupby('cluster_str').agg({
                    'temperatura': ['mean', 'std', 'min', 'max'],
                    'vibracao': ['mean', 'std'],
                    'distancia': ['mean', 'std'],
                    'estado_alerta': lambda x: (x == 'CRITICO').sum() # Conta críticos por cluster
                }).round(2)
                
                # Renomear colunas
                cluster_stats.columns = [
                    'Temp Média', 'Temp Desvio', 'Temp Mín', 'Temp Máx',
                    'Vib Média', 'Vib Desvio', 
                    'Dist Média', 'Dist Desvio',
                    'Alertas Críticos'
                ]
                
                st.dataframe(cluster_stats)
            
            else:
                 st.warning("Colunas 'temperatura' ou 'vibracao' não encontradas para análise de clusters.")
        else:
            st.warning("Coluna **'cluster'** não encontrada nos dados. O pipeline de ML (Clusterização) pode não ter sido executado.")

    # RESUMO EXECUTIVO
    st.markdown("---")
    st.subheader("📋 Resumo Executivo")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.write("**🔴 Situação Crítica:**")
        st.write(f"- **{criticos:,.0f}** registros em estado CRÍTICO")
        st.write(f"- Temperatura máxima: **{df['temperatura'].max():.1f}°C**")
    
    with col_res2:
        st.write("**🟠 Alertas:**")
        st.write(f"- **{alertas:,.0f}** registros requerem atenção")
        st.write(f"- **{anomalias:,.0f}** anomalias detectadas")
    
    with col_res3:
        st.write("**📊 Estatísticas:**")
        st.write(f"- Temperatura média: **{df['temperatura'].mean():.1f}°C**")
        st.write(f"- Vibração média: **{df['vibracao'].mean():.2f}**")
        
        # Garante que o período não falhe se a coluna timestamp existir mas estiver vazia/nula
        if not df['timestamp'].empty and df['timestamp'].min() is not pd.NaT:
             st.write(f"- Período: {df['timestamp'].min().strftime('%d/%m %H:%M')} a {df['timestamp'].max().strftime('%d/%m %H:%M')}")
        else:
            st.write("- Período: Indisponível (Timestamp nulo)")

else:
    st.error('''
    ⚠️ **Sistema não inicializado**

    O dashboard precisa de dados válidos. Por favor, verifique:

    1. **Estrutura do CSV:** Certifique-se que o arquivo CSV contém as colunas necessárias (`timestamp`, `temperatura`, `vibracao`, `estado_alerta`, `cluster`, etc.).
    2. **Localização do Arquivo:** Verifique se **'dados_finais_ml.csv'** existe na pasta raiz ou em um nível superior.
    3. **Upload:** Se o arquivo não estiver localmente, utilize o botão **'Carregar dados'** na barra lateral.
    ''')

# Rodapé
st.markdown('---')
st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')
