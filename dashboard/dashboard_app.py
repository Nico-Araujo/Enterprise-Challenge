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

# Cabeçalho
st.title('🚀 Monitoramento Inteligente - Hermes Reply')

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
                st.sidebar.success(f"✅ Arquivo encontrado em: {caminho}")
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
    # DEBUG: Mostrar informações sobre os dados
    st.sidebar.subheader("🔍 Debug Info")
    st.sidebar.write(f"Colunas: {list(df.columns)}")
    st.sidebar.write(f"Total de linhas: {len(df)}")
    st.sidebar.write(f"Primeiras linhas:")
    st.sidebar.dataframe(df.head(3))
    
    st.success(f"Dados carregados: {len(df)} registros")
    
    # KPIs - mais flexíveis
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Leituras', len(df))

    with col2:
        # Procurar coluna de alertas críticos
        coluna_criticos = next((col for col in df.columns if 'critic' in col.lower() or 'alerta' in col.lower()), None)
        criticos = len(df[df[coluna_criticos] == 'CRITICO']) if coluna_criticos else 0
        st.metric('Alertas Críticos', criticos)

    with col3:
        atencao = len(df[df[coluna_criticos] == 'ALERTA']) if coluna_criticos else 0
        st.metric('Alertas de Atenção', atencao)

    with col4:
        # Procurar coluna de anomalias
        coluna_anomalias = next((col for col in df.columns if 'anomal' in col.lower()), 'anomalia')
        anomalias = (df[coluna_anomalias] == -1).sum() if coluna_anomalias in df.columns else 0
        st.metric('Anomalias', anomalias)

    # Gráficos - mais flexíveis
    tab1, tab2, tab3, tab4 = st.tabs(['📈 Série Temporal', '🔍 Análise', '🚨 Alertas', '📊 Debug'])

    with tab1:
        # Encontrar colunas de temperatura e timestamp
        coluna_temp = next((col for col in df.columns if 'temp' in col.lower()), None)
        coluna_time = next((col for col in df.columns if 'time' in col.lower() or 'data' in col.lower() or 'hora' in col.lower()), None)
        
        if coluna_temp and coluna_time:
            fig_temp = px.line(df, x=coluna_time, y=coluna_temp, title=f'{coluna_temp} ao Longo do Tempo')
            st.plotly_chart(fig_temp, use_container_width=True)
        else:
            st.warning(f'Colunas de temperatura ou timestamp não encontradas. Colunas disponíveis: {list(df.columns)}')

    with tab2:
        # Encontrar coluna de vibração
        coluna_vib = next((col for col in df.columns if 'vibra' in col.lower() or 'acel' in col.lower()), None)
        
        if coluna_temp and coluna_vib:
            fig_scatter = px.scatter(df, x=coluna_temp, y=coluna_vib, 
                                   title=f'Relação {coluna_temp} vs {coluna_vib}')
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning(f'Colunas para scatter plot não encontradas. Colunas numéricas: {df.select_dtypes(include=["number"]).columns.tolist()}')

    with tab3:
        if coluna_criticos:
            alert_counts = df[coluna_criticos].value_counts()
            fig_alerts = px.pie(values=alert_counts.values, names=alert_counts.index, title='Distribuição de Alertas')
            st.plotly_chart(fig_alerts, use_container_width=True)
        else:
            st.warning('Coluna de alertas não encontrada')

    with tab4:
        st.subheader("Dados Completos")
        st.dataframe(df)
        st.subheader("Estatísticas")
        st.write(df.describe())
        st.subheader("Tipos de Dados")
        st.write(df.dtypes)

else:
    st.error("⚠️ SISTEMA NÃO INICIALIZADO")
    st.write("Para usar o dashboard:")
    st.write("1. Execute o pipeline de Machine Learning")
    st.write("2. Certifique-se que 'dados_finais_ml.csv' existe na pasta raiz")
    st.write("3. Ou faça upload do arquivo na sidebar")
    st.write("4. Recarregue esta página")

# Rodapé
st.markdown('---')
st.markdown('**Hermes Reply - Fase 6** | Pipeline Integrado: Sensores → ML → Dashboard')
