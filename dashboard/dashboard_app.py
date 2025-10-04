import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURAÇÃO DA PÁGINA E ESTILOS ---
st.set_page_config(
    page_title='Monitoramento Inteligente - Hermes Reply',
    page_icon='🚀',
    layout='wide'
)

ALERT_COLORS = {'NORMAL': '#2ca02c', 'ALERTA': '#ff7f0e', 'CRITICO': '#d62728'}
ANOMALY_COLORS = {'Normal': '#1f77b4', 'Anomalia': '#d62728'}

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border-left: 7px solid #1f77b4;
    }
    .stMetric > div > span {
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES ---

@st.cache_data
def load_data(uploaded_file):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Arquivo carregado com sucesso.")
        else:
            caminhos = ['dados_finais_ml.csv', '../dados_finais_ml.csv']
            for caminho in caminhos:
                if os.path.exists(caminho):
                    df = pd.read_csv(caminho)
                    st.success(f"✅ Arquivo local '{caminho}' carregado com sucesso.")
                    break
            else:
                return pd.DataFrame()

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Conversão de colunas numéricas
        for col in ['temperatura', 'vibracao', 'anomalia_score', 'distancia']:
            if col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                st.write(f"📌 {col}: {df[col].isna().sum()} valores nulos após conversão")

        return df

    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()


def display_kpis(df):
    st.subheader("Visão Geral")
    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    criticos = (df['estado_alerta'] == 'CRITICO').sum()
    alertas = (df['estado_alerta'] == 'ALERTA').sum()
    anomalias = (df['anomalia'] == -1).sum()

    col1.metric('Total de Leituras', f"{total:,}")
    col2.metric('Alertas Críticos', f"{criticos:,}", delta=f"{(criticos/total):.2%}")
    col3.metric('Alertas de Atenção', f"{alertas:,}", delta=f"{(alertas/total):.2%}")
    col4.metric('Anomalias Detectadas', f"{anomalias:,}", delta=f"{(anomalias/total):.2%}")


def display_main_charts(df):
    tab1, tab2, tab3 = st.tabs([
        '📈 Monitoramento Tempo Real',
        '🔍 Análise de Sensores',
        '🚨 Alertas & Anomalias'
    ])

    with tab1:
        st.subheader("Monitoramento em Tempo Real dos Sensores")
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig = px.line(df, x='timestamp', y='temperatura', title='Temperatura ao Longo do Tempo',
                          color_discrete_sequence=['#FF6B6B'])
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            if 'vibracao' in df.columns:
                fig = px.line(df, x='timestamp', y='vibracao', title='Vibração ao Longo do Tempo',
                              color_discrete_sequence=['#4ECDC4'])
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'distancia' in df.columns:
                fig = px.line(df, x='timestamp', y='distancia', title='Distância ao Longo do Tempo',
                              color_discrete_sequence=['#45B7D1'])
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Análise de Correlação entre Sensores")
        required_cols = ['temperatura', 'vibracao', 'estado_alerta']
        if all(col in df.columns for col in required_cols):
            plot_df = df.dropna(subset=required_cols)
            if not plot_df.empty:
                fig = px.scatter(
                    plot_df,
                    x='temperatura',
                    y='vibracao',
                    color='estado_alerta',
                    title='Temperatura vs Vibração',
                    color_discrete_map=ALERT_COLORS
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("❗ Dados insuficientes para exibir o gráfico (dados nulos ou ausentes).")
                st.dataframe(df[required_cols].head(10))
        else:
            st.warning("❗ Colunas ausentes para o gráfico: " + ", ".join(
                [col for col in required_cols if col not in df.columns]
            ))

    with tab3:
        st.subheader("Alertas e Anomalias")

        col1, col2 = st.columns(2)
        with col1:
            if 'estado_alerta' in df.columns:
                fig = px.pie(df, names='estado_alerta', title='Distribuição de Estados de Alerta',
                             color_discrete_map=ALERT_COLORS)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'anomalia_score' in df.columns and 'status_anomalia' in df.columns:
                fig = px.scatter(df, x='timestamp', y='anomalia_score', color='status_anomalia',
                                 title='Scores de Anomalia ao Longo do Tempo',
                                 color_discrete_map=ANOMALY_COLORS)
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Registros com Alertas Críticos")
        crit_df = df[df['estado_alerta'] == 'CRITICO']
        if not crit_df.empty:
            cols = [c for c in ['timestamp', 'temperatura', 'vibracao', 'distancia', 'anomalia_score'] if c in crit_df.columns]
            st.dataframe(crit_df[cols].sort_values('temperatura', ascending=False))
        else:
            st.info("✅ Nenhum alerta crítico encontrado.")


def display_summary(df):
    st.markdown("---")
    st.subheader("📋 Resumo Executivo")

    if not all(col in df.columns for col in ['estado_alerta', 'anomalia', 'temperatura', 'timestamp']):
        st.warning("❌ Colunas essenciais ausentes para gerar o resumo.")
        return

    criticos = (df['estado_alerta'] == 'CRITICO').sum()
    alertas = (df['estado_alerta'] == 'ALERTA').sum()
    anomalias = (df['anomalia'] == -1).sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🔴 Situação Crítica:**")
        st.markdown(f"- {criticos} registros críticos")
        st.markdown(f"- Temperatura máx: {df['temperatura'].max():.1f}°C")

    with col2:
        st.markdown("**🟠 Alertas e Anomalias:**")
        st.markdown(f"- {alertas} registros em alerta")
        st.markdown(f"- {anomalias} anomalias detectadas")

    with col3:
        st.markdown("**📊 Estatísticas Gerais:**")
        st.markdown(f"- Temperatura média: {df['temperatura'].mean():.1f}°C")
        st.markdown(f"- Período: {df['timestamp'].min():%d/%m/%Y %H:%M} → {df['timestamp'].max():%d/%m/%Y %H:%M}")


# --- APP STREAMLIT ---
def main():
    st.markdown('<h1 class="main-header">🚀 Monitoramento Inteligente - Hermes Reply</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.title("⚙️ Controles")
        uploaded_file = st.file_uploader("Carregar CSV de dados", type=["csv", "txt"])

    df = load_data(uploaded_file)

    if not df.empty:
        display_kpis(df)
        display_main_charts(df)
        display_summary(df)
    else:
        st.error("⚠️ Nenhum dado carregado. Faça o upload de um CSV com os dados esperados.")

    st.markdown("---")
    st.markdown("**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard")


if __name__ == "__main__":
    main()
