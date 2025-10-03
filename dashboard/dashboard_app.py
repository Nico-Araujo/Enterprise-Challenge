import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

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
    # DEBUG: Mostrar informações detalhadas
    st.sidebar.subheader("🔍 Debug Info")
    st.sidebar.write(f"Colunas: {list(df.columns)}")
    st.sidebar.write(f"Total de linhas: {len(df)}")
    
    # Encontrar colunas relevantes
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
    
    st.sidebar.write(f"Colunas numéricas: {colunas_numericas}")
    st.sidebar.write(f"Colunas texto: {colunas_texto}")
    
    st.success(f"Dados carregados: {len(df)} registros")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Leituras', len(df))

    with col2:
        st.metric('Colunas Disponíveis', len(df.columns))

    with col3:
        st.metric('Colunas Numéricas', len(colunas_numericas))

    with col4:
        st.metric('Colunas Texto', len(colunas_texto))

    # Gráficos - CORRIGIDO
    tab1, tab2, tab3 = st.tabs(['📈 Gráficos Principais', '📊 Dados Completos', '🔍 Análise'])

    with tab1:
        st.subheader("Visualizações dos Dados")
        
        # GRÁFICO 1: Encontrar colunas de sensores (temperatura, vibração, etc.)
        colunas_sensor = [col for col in colunas_numericas if any(word in col.lower() for word in 
                        ['temp', 'vibra', 'acel', 'press', 'corrente', 'tensao', 'rpm', 'veloc'])]
        
        if len(colunas_sensor) >= 2:
            col1_graf, col2_graf = st.columns(2)
            
            with col1_graf:
                # Scatter plot entre dois sensores
                sensor_x = st.selectbox("Eixo X:", colunas_sensor, index=0)
                sensor_y = st.selectbox("Eixo Y:", colunas_sensor, index=min(1, len(colunas_sensor)-1))
                
                fig_scatter = px.scatter(df, x=sensor_x, y=sensor_y, 
                                       title=f'{sensor_x} vs {sensor_y}')
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2_graf:
                # Histograma do primeiro sensor
                sensor_hist = st.selectbox("Histograma:", colunas_sensor, index=0)
                fig_hist = px.histogram(df, x=sensor_hist, title=f'Distribuição de {sensor_hist}')
                st.plotly_chart(fig_hist, use_container_width=True)
                
        elif colunas_sensor:
            # Se só tem uma coluna de sensor
            sensor = colunas_sensor[0]
            fig_hist = px.histogram(df, x=sensor, title=f'Distribuição de {sensor}')
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("Nenhuma coluna de sensor identificada. Mostrando primeiras colunas numéricas:")
            if len(colunas_numericas) >= 2:
                fig_scatter = px.scatter(df, x=colunas_numericas[0], y=colunas_numericas[1])
                st.plotly_chart(fig_scatter, use_container_width=True)

        # GRÁFICO 2: Série temporal se tiver timestamp
        coluna_tempo = next((col for col in df.columns if any(word in col.lower() for word in 
                          ['time', 'data', 'hora', 'timestamp', 'date'])), None)
        
        if coluna_tempo and colunas_sensor:
            st.subheader("Série Temporal")
            sensor_tempo = st.selectbox("Sensor para série temporal:", colunas_sensor, key='temp_sensor')
            
            # Tentar converter para datetime se possível
            try:
                if df[coluna_tempo].dtype == 'object':
                    df_temp = df.copy()
                    # Tentar converter timestamp milissegundos
                    if df[coluna_tempo].astype(str).str.contains('1.7').any():
                        df_temp[coluna_tempo] = pd.to_datetime(df[coluna_tempo].astype(float), unit='ms')
                    else:
                        df_temp[coluna_tempo] = pd.to_datetime(df[coluna_tempo])
                    
                    fig_time = px.line(df_temp, x=coluna_tempo, y=sensor_tempo, 
                                     title=f'{sensor_tempo} ao Longo do Tempo')
                    st.plotly_chart(fig_time, use_container_width=True)
                else:
                    fig_time = px.line(df, x=coluna_tempo, y=sensor_tempo, 
                                     title=f'{sensor_tempo} ao Longo do Tempo')
                    st.plotly_chart(fig_time, use_container_width=True)
            except:
                # Se falhar a conversão, usar como numérico
                fig_time = px.line(df, x=coluna_tempo, y=sensor_tempo, 
                                 title=f'{sensor_tempo} vs {coluna_tempo}')
                st.plotly_chart(fig_time, use_container_width=True)

    with tab2:
        st.subheader("Dados Completos")
        st.dataframe(df)
        
        st.subheader("Estatísticas Descritivas")
        st.write(df.describe())

    with tab3:
        st.subheader("Análise de Valores")
        
        # Mostrar valores únicos para colunas numéricas
        st.write("**Colunas Numéricas:**")
        for coluna in colunas_numericas:
            with st.expander(f"📊 {coluna}"):
                col1_info, col2_info = st.columns(2)
                with col1_info:
                    st.write(f"Mínimo: {df[coluna].min():.2f}")
                    st.write(f"Máximo: {df[coluna].max():.2f}")
                    st.write(f"Média: {df[coluna].mean():.2f}")
                with col2_info:
                    st.write(f"Desvio Padrão: {df[coluna].std():.2f}")
                    st.write(f"Valores Únicos: {df[coluna].nunique()}")
                    st.write(f"Valores Nulos: {df[coluna].isna().sum()}")

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
