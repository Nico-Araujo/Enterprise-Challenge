import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title='Teste Gráfico Pizza', layout='wide')
st.title('🧪 Teste - Gráfico de Pizza de Alertas')

# Carregar dados - APENAS DO CAMINHO PRINCIPAL
@st.cache_data
def load_data():
    try:
        # APENAS UM CAMINHO: a pasta raiz do repositório
        caminho = 'dados_finais_ml.csv'
        
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            st.success(f"✅ Arquivo encontrado em: {caminho}")
            return df
        else:
            st.error(f"❌ Arquivo não encontrado em: {caminho}")
            st.info("📁 Certifique-se que 'dados_finais_ml.csv' está na pasta raiz do seu repositório")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f'Erro ao carregar dados: {e}')
        return pd.DataFrame()

df = load_data()

if not df.empty and 'estado_alerta' in df.columns:
    st.success(f"✅ Dados carregados: {len(df)} registros")
    
    # MÉTODO 1: Contagem manual explícita
    st.subheader("Método 1: Contagem Manual")
    
    normal_count = len(df[df['estado_alerta'] == 'NORMAL'])
    alerta_count = len(df[df['estado_alerta'] == 'ALERTA'])
    critico_count = len(df[df['estado_alerta'] == 'CRITICO'])
    
    st.write(f"**Contagens manuais:**")
    st.write(f"- NORMAL: {normal_count}")
    st.write(f"- ALERTA: {alerta_count}") 
    st.write(f"- CRITICO: {critico_count}")
    st.write(f"- Total: {normal_count + alerta_count + critico_count}")
    
    # Gráfico 1: Versão mais simples
    st.subheader("Gráfico de Pizza - Versão Simplificada")
    try:
        fig = px.pie(
            values=[normal_count, alerta_count, critico_count],
            names=['NORMAL', 'ALERTA', 'CRITICO'],
            title='Distribuição de Estados de Alerta',
            color=['NORMAL', 'ALERTA', 'CRITICO'],
            color_discrete_map={'NORMAL': 'green', 'ALERTA': 'orange', 'CRITICO': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ Gráfico de pizza criado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro no gráfico de pizza: {e}")

else:
    if df.empty:
        st.error('⚠️ Nenhum dado foi carregado')
    else:
        st.error('⚠️ Coluna "estado_alerta" não encontrada nos dados')
    
    # Mostrar debug info
    st.subheader("🔍 Informações para Debug")
    if not df.empty:
        st.write(f"📊 Total de registros carregados: {len(df)}")
        st.write(f"📋 Colunas disponíveis: {list(df.columns)}")
        st.write("👀 Primeiras linhas dos dados:")
        st.dataframe(df.head(3))
    else:
        st.write("❌ Nenhum dado disponível para mostrar")

# Verificação da estrutura de arquivos
st.subheader("📁 Verificação de Estrutura")
st.write("Estrutura esperada:")
st.code("""
seu-repositorio/
├── dados_finais_ml.csv     ← Arquivo deve estar AQUI
├── dashboard/
│   └── app.py             ← Este arquivo
└── README.md
""")

st.write("Verificando se o arquivo existe...")
if os.path.exists('dados_finais_ml.csv'):
    st.success("✅ 'dados_finais_ml.csv' encontrado na pasta raiz!")
else:
    st.error("❌ 'dados_finais_ml.csv' NÃO encontrado na pasta raiz")
