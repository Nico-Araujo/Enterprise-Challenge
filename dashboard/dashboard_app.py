import streamlit as st
import pandas as pd
import plotly.express as px
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
        # Tentar vários caminhos possíveis
        caminhos = [
            '../dados_finais_ml.csv',  # Pasta raiz
            'dados_finais_ml.csv',     # Pasta atual
        ]
        
        for caminho in caminhos:
            if os.path.exists(caminho):
                df = pd.read_csv(caminho)
                st.success(f"✅ Arquivo encontrado em: {caminho}")
                return df
        
        # Se usuário fez upload
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        
        return pd.DataFrame()

    except Exception as e:
        st.error(f'Erro ao carregar dados: {str(e)}')
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.success(f"Dados carregados: {len(df)} registros")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Leituras', len(df))

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
    tab1, tab2, tab3 = st.tabs(['📈 Série Temporal', '🔍 Análise', '🚨 Alertas'])

    with tab1:
        if 'temperatura' in df.columns and 'data_hora_ms' in df.columns:
            fig_temp = px.line(df, x='data_hora_ms', y='temperatura', title='Temperatura ao Longo do Tempo')
            st.plotly_chart(fig_temp, use_container_width=True)
        else:
            st.warning('Dados de temperatura ou timestamp não disponíveis')

    with tab2:
        if all(col in df.columns for col in ['temperatura', 'vibracao']):
            fig_scatter = px.scatter(df, x='temperatura', y='vibracao', title='Relação Temperatura vs Vibração')
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning('Dados de temperatura ou vibração não disponíveis')

    with tab3:
        if 'estado_alerta' in df.columns:
            alert_counts = df['estado_alerta'].value_counts()
            fig_alerts = px.pie(values=alert_counts.values, names=alert_counts.index, title='Distribuição de Alertas')
            st.plotly_chart(fig_alerts, use_container_width=True)
        else:
            st.warning('Dados de alerta não disponíveis')

else:
    st.error("⚠️ SISTEMA NÃO INICIALIZADO")
    st.write("Para usar o dashboard:")
    st.write("1. Execute o pipeline de Machine Learning")
    st.write("2. Certifique-se que 'dados_finais_ml.csv' existe na pasta raiz")
    st.write("3. Ou faça upload do arquivo na sidebar")
    st.write("4. Recarregue esta página")

# Rodapé
st.markdown('---')
st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')
