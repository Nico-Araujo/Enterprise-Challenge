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
    # DEBUG: Mostrar informações detalhadas
    st.sidebar.subheader("🔍 Debug Info")
    st.sidebar.write(f"Colunas: {list(df.columns)}")
    st.sidebar.write(f"Total de linhas: {len(df)}")
    st.sidebar.write(f"Tipos de dados:")
    st.sidebar.write(df.dtypes)
    
    st.success(f"Dados carregados: {len(df)} registros")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Leituras', len(df))

    with col2:
        st.metric('Colunas Disponíveis', len(df.columns))

    with col3:
        colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
        st.metric('Colunas Numéricas', len(colunas_numericas))

    with col4:
        colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
        st.metric('Colunas Texto', len(colunas_texto))

    # Gráficos - DEBUG DETALHADO
    tab1, tab2, tab3 = st.tabs(['📈 Debug Gráficos', '📊 Dados Completos', '🔍 Análise'])

    with tab1:
        st.subheader("Teste de Gráficos")
        
        # Teste 1: Gráfico simples com primeiras colunas numéricas
        colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
        st.write(f"Colunas numéricas disponíveis: {colunas_numericas}")
        
        if len(colunas_numericas) >= 2:
            col_x = colunas_numericas[0]
            col_y = colunas_numericas[1]
            
            st.write(f"Tentando plotar: {col_x} vs {col_y}")
            st.write(f"Valores únicos em {col_x}: {df[col_x].nunique()}")
            st.write(f"Valores únicos em {col_y}: {df[col_y].nunique()}")
            
            # Verificar se há dados válidos
            if df[col_x].notna().any() and df[col_y].notna().any():
                try:
                    fig_test = px.scatter(df, x=col_x, y=col_y, title=f'Teste: {col_x} vs {col_y}')
                    st.plotly_chart(fig_test, use_container_width=True)
                    st.success("✅ Gráfico de teste plotado com sucesso!")
                except Exception as e:
                    st.error(f"❌ Erro ao plotar gráfico: {e}")
            else:
                st.warning("⚠️ Dados contêm valores NaN")
                
        else:
            st.error("❌ Não há colunas numéricas suficientes para plotar")

        # Teste 2: Histograma simples
        if colunas_numericas:
            col_hist = colunas_numericas[0]
            st.write(f"Histograma de {col_hist}")
            fig_hist = px.histogram(df, x=col_hist, title=f'Distribuição de {col_hist}')
            st.plotly_chart(fig_hist, use_container_width=True)

    with tab2:
        st.subheader("Dados Completos")
        st.dataframe(df)
        
        st.subheader("Estatísticas Descritivas")
        st.write(df.describe())
        
        st.subheader("Info do DataFrame")
        st.write(f"Shape: {df.shape}")
        st.write(f"Colunas: {list(df.columns)}")
        st.write("Tipos de dados:")
        st.write(df.dtypes)

    with tab3:
        st.subheader("Análise de Valores")
        
        # Mostrar valores únicos para cada coluna
        for coluna in df.columns:
            with st.expander(f"Coluna: {coluna} ({df[coluna].dtype})"):
                st.write(f"Valores únicos: {df[coluna].nunique()}")
                st.write(f"Valores nulos: {df[coluna].isna().sum()}")
                if df[coluna].nunique() <= 20:  # Mostrar valores se não forem muitos
                    st.write(f"Valores: {df[coluna].unique()}")
                else:
                    st.write(f"Primeiros valores: {df[coluna].head(10).tolist()}")

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
