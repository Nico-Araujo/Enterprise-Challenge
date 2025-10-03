import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# Configuração da página
st.set_page_config(
    page_title='Debug - Dados ML',
    page_icon='🔍',
    layout='wide'
)

st.title('🔍 Debug Completo - Análise dos Dados')

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
                st.sidebar.success(f"✅ Arquivo encontrado em: {caminho}")
                return df
        
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        
        return pd.DataFrame()

    except Exception as e:
        st.error(f'Erro ao carregar dados: {str(e)}')
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # ANÁLISE COMPLETA DOS DADOS
    st.header("📊 Análise Completa do DataFrame")
    
    # Informações básicas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Linhas", len(df))
    with col2:
        st.metric("Total de Colunas", len(df.columns))
    with col3:
        st.metric("Colunas Numéricas", len(df.select_dtypes(include=[np.number]).columns))
    with col4:
        st.metric("Memória Usada", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # TAB 1: ESTRUTURA DOS DADOS
    tab1, tab2, tab3, tab4 = st.tabs(['🏗️ Estrutura', '📈 Valores', '🔍 Problemas', '🎯 Gráficos Teste'])
    
    with tab1:
        st.subheader("Estrutura do DataFrame")
        
        # Mostrar primeiras e últimas linhas
        col_prev, col_next = st.columns(2)
        with col_prev:
            st.write("**Primeiras 5 linhas:**")
            st.dataframe(df.head())
        with col_next:
            st.write("**Últimas 5 linhas:**")
            st.dataframe(df.tail())
        
        # Info detalhada das colunas
        st.subheader("Informações das Colunas")
        info_data = []
        for coluna in df.columns:
            info_data.append({
                'Coluna': coluna,
                'Tipo': str(df[coluna].dtype),
                'Não Nulos': df[coluna].notna().sum(),
                'Nulos': df[coluna].isna().sum(),
                'Valores Únicos': df[coluna].nunique(),
                'Exemplo': str(df[coluna].iloc[0]) if len(df) > 0 else 'N/A'
            })
        st.dataframe(pd.DataFrame(info_data))
    
    with tab2:
        st.subheader("Valores e Distribuições")
        
        # Para cada coluna, mostrar análise detalhada
        for coluna in df.columns:
            with st.expander(f"📋 {coluna} ({df[coluna].dtype})", expanded=False):
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.write("**Estatísticas:**")
                    if pd.api.types.is_numeric_dtype(df[coluna]):
                        st.write(f"- Mínimo: {df[coluna].min()}")
                        st.write(f"- Máximo: {df[coluna].max()}")
                        st.write(f"- Média: {df[coluna].mean():.2f}")
                        st.write(f"- Mediana: {df[coluna].median():.2f}")
                        st.write(f"- Desvio Padrão: {df[coluna].std():.2f}")
                    else:
                        st.write(f"- Valores únicos: {df[coluna].nunique()}")
                        st.write(f"- Valor mais frequente: {df[coluna].mode().iloc[0] if len(df[coluna].mode()) > 0 else 'N/A'}")
                
                with col_right:
                    st.write("**Amostra de Valores:**")
                    unique_vals = df[coluna].unique()
                    if len(unique_vals) <= 10:
                        st.write(list(unique_vals))
                    else:
                        st.write(f"Primeiros 10: {list(unique_vals[:10])}")
                        
                    # Mostrar histograma para numéricas
                    if pd.api.types.is_numeric_dtype(df[coluna]):
                        fig = px.histogram(df, x=coluna, title=f'Distribuição de {coluna}')
                        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Problemas Identificados")
        
        problemas = []
        
        # Verificar problemas em cada coluna
        for coluna in df.columns:
            # Valores nulos
            nulos = df[coluna].isna().sum()
            if nulos > 0:
                problemas.append(f"❌ **{coluna}**: {nulos} valores nulos")
            
            # Verificar se coluna numérica tem valores suspeitos
            if pd.api.types.is_numeric_dtype(df[coluna]):
                zeros = (df[coluna] == 0).sum()
                negativos = (df[coluna] < 0).sum()
                
                if zeros > len(df) * 0.8:  # Mais de 80% zeros
                    problemas.append(f"⚠️ **{coluna}**: Muitos zeros ({zeros}/{len(df)})")
                
                if negativos > 0 and 'temp' in coluna.lower():
                    problemas.append(f"❌ **{coluna}**: Temperatura com valores negativos")
            
            # Verificar timestamps
            if any(word in coluna.lower() for word in ['time', 'data', 'hora', 'timestamp']):
                unique_vals = df[coluna].unique()
                if len(unique_vals) < 5:
                    problemas.append(f"⚠️ **{coluna}**: Poucos valores únicos para timestamp")
                
                # Verificar formato estranho
                sample_val = str(df[coluna].iloc[0])
                if '1.75944' in sample_val:
                    problemas.append(f"❌ **{coluna}**: Timestamp em formato incorreto (milissegundos não convertidos)")
        
        if problemas:
            st.error("Problemas encontrados:")
            for problema in problemas:
                st.write(problema)
        else:
            st.success("✅ Nenhum problema crítico identificado")
    
    with tab4:
        st.subheader("Testes de Gráficos")
        
        # Testar diferentes combinações de colunas
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(colunas_numericas) >= 2:
            st.write("**Teste 1: Scatter Plot**")
            col_x = st.selectbox("Eixo X", colunas_numericas, key='scatter_x')
            col_y = st.selectbox("Eixo Y", colunas_numericas, key='scatter_y')
            
            # Verificar se os dados fazem sentido para scatter plot
            if df[col_x].nunique() > 1 and df[col_y].nunique() > 1:
                fig = px.scatter(df, x=col_x, y=col_y, title=f'{col_x} vs {col_y}')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Dados não variam suficiente para scatter plot")
        
        # Testar série temporal
        colunas_tempo = [col for col in df.columns if any(word in col.lower() for word in ['time', 'data', 'hora'])]
        if colunas_tempo and colunas_numericas:
            st.write("**Teste 2: Série Temporal**")
            col_tempo = st.selectbox("Coluna de Tempo", colunas_tempo)
            col_valor = st.selectbox("Coluna de Valor", colunas_numericas, key='time_val')
            
            # Tentar converter timestamp
            try:
                if df[col_tempo].dtype == 'object' and df[col_tempo].str.contains('1.7').any():
                    df_temp = df.copy()
                    df_temp[col_tempo] = pd.to_datetime(df_temp[col_tempo].astype(float), unit='ms')
                    fig = px.line(df_temp, x=col_tempo, y=col_valor, title=f'{col_valor} ao longo do tempo')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.line(df, x=col_tempo, y=col_valor, title=f'{col_valor} vs {col_tempo}')
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao criar série temporal: {e}")

else:
    st.error("Nenhum dado carregado")

# Rodapé
st.markdown('---')
st.markdown('**Debug Tool** | Análise completa dos dados')
