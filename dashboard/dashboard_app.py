import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA E ESTILOS ---
st.set_page_config(
    page_title='Monitoramento Inteligente - Hermes Reply',
    page_icon='🚀',
    layout='wide'
)

# Cores padrão para os gráficos para manter a consistência
ALERT_COLORS = {'NORMAL': '#2ca02c', 'ALERTA': '#ff7f0e', 'CRITICO': '#d62728'}
ANOMALY_COLORS = {'Normal': '#1f77b4', 'Anomalia': '#d62728'}

# CSS personalizado para melhorar a aparência
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

# --- FUNÇÕES AUXILIARES ---

@st.cache_data
def load_data(uploaded_file):
    df = None
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Arquivo enviado pelo usuário carregado com sucesso!")
        else:
            caminhos = ['dados_finais_ml.csv', '../dados_finais_ml.csv']
            for caminho in caminhos:
                if os.path.exists(caminho):
                    df = pd.read_csv(caminho)
                    st.success(f"✅ Arquivo local '{caminho}' carregado com sucesso!")
                    break

        if df is not None:
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Conversão de colunas numéricas
            numeric_cols = ['temperatura', 'vibracao', 'anomalia_score', 'distancia']
            for col in numeric_cols:
                if col in df.columns:
                    if df[col].dtype == 'object':
                        df[col] = df[col].str.replace(',', '.', regex=False)
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Debug temporário
                    st.write(f"📊 Coluna `{col}`: {df[col].isna().sum()} valores nulos após conversão.")

            return df

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar o arquivo: {e}")
    
    return pd.DataFrame()


def display_kpis(df):
    st.subheader("Visão Geral")
    col1, col2, col3, col4 = st.columns(4)

    total_leituras = len(df)
    if total_leituras == 0:
        st.warning("Não há dados para exibir os KPIs.")
        return

    criticos = (df['estado_alerta'] == 'CRITICO').sum()
    alertas = (df['estado_alerta'] == 'ALERTA').sum()
    anomalias = (df['anomalia'] == -1).sum()

    with col1:
        st.metric('Total de Leituras', f'{total_leituras:,}')
    with col2:
        st.metric('Alertas Críticos', f'{criticos:,}', delta=f"{criticos/total_leituras:.2%}", delta_color="inverse")
    with col3:
        st.metric('Alertas de Atenção', f'{alertas:,}', delta=f"{alertas/total_leituras:.2%}", delta_color="inverse")
    with col4:
        st.metric('Anomalias Detectadas', f'{anomalias:,}', delta=f"{anomalias/total_leituras:.2%}", delta_color="inverse")


def display_main_charts(df):
    tab1, tab2, tab3 = st.tabs(['📈 Monitoramento Tempo Real', '🔍 Análise de Sensores', '🚨 Alertas & Anomalias'])

    with tab1:
        st.subheader("Monitoramento em Tempo Real dos Sensores")
        if 'timestamp' in df.columns and 'temperatura' in df.columns:
            fig_temp = px.line(df, x='timestamp', y='temperatura', title='Temperatura ao Longo do Tempo', color_discrete_sequence=['#FF6B6B'])
            fig_temp.add_hline(y=df['temperatura'].mean() + 2 * df['temperatura'].std(), line_dash="dash", line_color="red", annotation_text="Limite Crítico (Exemplo)")
            st.plotly_chart(fig_temp, use_container_width=True)

        col1_sens, col2_sens = st.columns(2)
        with col1_sens:
            if 'vibracao' in df.columns:
                fig_vib = px.line(df, x='timestamp', y='vibracao', title='Vibração ao Longo do Tempo', color_discrete_sequence=['#4ECDC4'])
                st.plotly_chart(fig_vib, use_container_width=True)
        with col2_sens:
            if 'distancia' in df.columns:
                fig_dist = px.line(df, x='timestamp', y='distancia', title='Distância ao Longo do Tempo', color_discrete_sequence=['#45B7D1'])
                st.plotly_chart(fig_dist, use_container_width=True)

    with tab2:
        st.subheader("Análise de Correlação entre Sensores")

        required_cols = ['temperatura', 'vibracao', 'estado_alerta']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if not missing_cols:
            # Conversão garantida de novo para segurança
            df['temperatura'] = pd.to_numeric(df['temperatura'], errors='coerce')
            df['vibracao'] = pd.to_numeric(df['vibracao'], errors='coerce')

            plot_df = df.dropna(subset=required_cols)

            if plot_df.empty:
                st.warning("❌ Após remoção de valores nulos, não há dados suficientes para o gráfico 'Temperatura vs Vibração'.")
                st.dataframe(df[required_cols].head(10))  # Debug opcional
            else:
                fig_scatter = px.scatter(
                    plot_df,
                    x='temperatura',
                    y='vibracao',
                    color='estado_alerta',
                    title='Temperatura vs Vibração (Colorido por Alerta)',
                    color_discrete_map=ALERT_COLORS
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning(f"⚠️ O gráfico 'Temperatura vs Vibração' não pode ser exibido. Colunas ausentes: **{', '.join(missing_cols)}**.")

    with tab3:
        st.subheader("Dashboard de Alertas e Anomalias")
        col1_alert, col2_alert = st.columns(2)

        with col1_alert:
            if 'estado_alerta' in df.columns:
                fig_alerts = px.pie(df, names='estado_alerta', title='Distribuição de Estados de Alerta',
                                    color='estado_alerta', color_discrete_map=ALERT_COLORS)
                fig_alerts.update_traces(textinfo='percent+label', insidetextorientation='radial')
                st.plotly_chart(fig_alerts, use_container_width=True)

        with col2_alert:
            if 'anomalia_score' in df.columns and 'status_anomalia' in df.columns:
                fig_anom = px.scatter(df, x='timestamp', y='anomalia_score', color='status_anomalia',
                                      title='Scores de Anomalia ao Longo do Tempo',
                                      color_discrete_map=ANOMALY_COLORS)
                st.plotly_chart(fig_anom, use_container_width=True)

        st.subheader("Registros com Alertas Críticos")
        criticos_df = df[df['estado_alerta'] == 'CRITICO']
        if not criticos_df.empty:
            display_cols = ['timestamp', 'temperatura', 'vibracao', 'distancia', 'anomalia_score']
            existing_cols = [col for col in display_cols if col in criticos_df.columns]
            st.dataframe(criticos_df[existing_cols].sort_values('temperatura', ascending=False))
        else:
            st.info("✅ Nenhum alerta crítico detectado.")


def display_summary(df):
    st.markdown("---")
    st.subheader("📋 Resumo Executivo")

    if 'estado_alerta' not in df.columns or 'anomalia' not in df.columns or 'temperatura' not in df.columns:
        st.warning("Não foi possível gerar o resumo. Colunas essenciais estão faltando.")
        return

    criticos = (df['estado_alerta'] == 'CRITICO').sum()
    alertas = (df['estado_alerta'] == 'ALERTA').sum()
    anomalias = (df['anomalia'] == -1).sum()

    col_res1, col_res2, col_res3 = st.columns(3)

    with col_res1:
        st.markdown(f"**🔴 Situação Crítica:**")
        st.markdown(f"- **{criticos}** registros em estado CRÍTICO.")
        st.markdown(f"- Temperatura máxima: **{df['temperatura'].max():.1f}°C**")

    with col_res2:
        st.markdown(f"**🟠 Alertas e Anomalias:**")
        st.markdown(f"- **{alertas}** registros requerem atenção.")
        st.markdown(f"- **{anomalias}** anomalias detectadas pelo modelo.")

    with col_res3:
        st.markdown(f"**📊 Estatísticas Gerais:**")
        st.markdown(f"- Temperatura média: **{df['temperatura'].mean():.1f}°C**")
        st.markdown(f"- Período analisado: **{df['timestamp'].min():%d/%m/%y %H:%M}** a **{df['timestamp'].max():%d/%m/%y %H:%M}**")


# --- FUNÇÃO PRINCIPAL ---
def main():
    st.markdown('<h1 class="main-header">🚀 Monitoramento Inteligente - Hermes Reply</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.title('⚙️ Controles')
        uploaded_file = st.file_uploader('Carregar arquivo de dados', type=['csv', 'txt'])

    df = load_data(uploaded_file)

    if not df.empty:
        display_kpis(df)
        st.markdown("---")
        display_main_charts(df)
        display_summary(df)
    else:
        st.error(
            """
            ⚠️ **Sistema não inicializado: Nenhum dado encontrado.**

            Para usar o dashboard, por favor:
            1. **Faça o upload de um arquivo CSV** usando o botão na barra lateral.
            2. Ou garanta que o arquivo `dados_finais_ml.csv` esteja na mesma pasta que o script.
            """
        )

    st.markdown('---')
    st.markdown('**Hermes Reply - Fase 4** | Pipeline Integrado: Sensores → ML → Dashboard')


if __name__ == "__main__":
    main()
