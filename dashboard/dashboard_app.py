import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração básica
st.set_page_config(page_title='Monitoramento Inteligente', layout='wide')
st.title('🚀 Monitoramento Inteligente - Hermes Reply')

# Carregar dados
@st.cache_data
def load_data():
    try:
        caminhos = ['../dados_finais_ml.csv', 'dados_finais_ml.csv']
        for caminho in caminhos:
            if os.path.exists(caminho):
                df = pd.read_csv(caminho)
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f'Erro: {e}')
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric('Total', len(df))
    with col2: st.metric('Críticos', len(df[df['estado_alerta'] == 'CRITICO']))
    with col3: st.metric('Alertas', len(df[df['estado_alerta'] == 'ALERTA']))
    with col4: st.metric('Anomalias', len(df[df['anomalia'] == -1]))

    tab1, tab2, tab3, tab4 = st.tabs(['📈 Tempo Real', '🔍 Sensores', '🚨 Alertas', '📊 Clusters'])

    with tab1:
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig = px.line(df, x='timestamp', y='temperatura', title='Temperatura')
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Temperatura vs Vibração")
        
        # VERIFICAÇÃO DOS DADOS
        st.write("**Verificação dos dados:**")
        st.write(f"- Primeira temperatura: {df['temperatura'].iloc[0]}")
        st.write(f"- Primeira vibração: {df['vibracao'].iloc[0]}")
        st.write(f"- Primeiro estado_alerta: {df['estado_alerta'].iloc[0]}")
        
        # GRÁFICO SIMPLES E DIRETO
        try:
            # Criar um scatter plot básico
            fig = px.scatter(
                df,
                x=df['temperatura'],
                y=df['vibracao'],
                title='Temperatura vs Vibração'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Gráfico básico criado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro no gráfico básico: {e}")

        # TENTAR COM CORES
        try:
            fig = px.scatter(
                df,
                x='temperatura',
                y='vibracao',
                color='estado_alerta',
                title='Temperatura vs Vibração (com cores)'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Gráfico colorido criado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro no gráfico colorido: {e}")

    with tab3:
        st.subheader("Distribuição de Alertas")
        
        # CONTAGEM MANUAL
        contagens = {
            'NORMAL': len(df[df['estado_alerta'] == 'NORMAL']),
            'ALERTA': len(df[df['estado_alerta'] == 'ALERTA']),
            'CRITICO': len(df[df['estado_alerta'] == 'CRITICO'])
        }
        
        st.write("**Contagens manuais:**")
        for estado, count in contagens.items():
            st.write(f"- {estado}: {count}")
        
        # GRÁFICO DE PIZZA DIRETO
        try:
            fig = px.pie(
                values=list(contagens.values()),
                names=list(contagens.keys()),
                title='Distribuição de Alertas'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Gráfico de pizza criado!")
        except Exception as e:
            st.error(f"❌ Erro no gráfico de pizza: {e}")

    with tab4:
        st.subheader("Análise de Clusters")
        
        if 'cluster' in df.columns:
            # CONTAGEM DE CLUSTERS
            clusters_unicos = df['cluster'].unique()
            st.write(f"Clusters únicos: {clusters_unicos}")
            
            contagem_clusters = df['cluster'].value_counts()
            st.write("Contagem por cluster:")
            for cluster, count in contagem_clusters.items():
                st.write(f"- Cluster {cluster}: {count}")
            
            # GRÁFICO DE BARRAS SIMPLES
            try:
                fig = px.bar(
                    x=contagem_clusters.index.astype(str),
                    y=contagem_clusters.values,
                    title='Distribuição de Clusters',
                    labels={'x': 'Cluster', 'y': 'Quantidade'}
                )
                st.plotly_chart(fig, use_container_width=True)
                st.success("✅ Gráfico de barras criado!")
            except Exception as e:
                st.error(f"❌ Erro no gráfico de barras: {e}")

else:
    st.error('⚠️ Nenhum dado carregado')

st.markdown('---')
st.markdown('**Hermes Reply**')
