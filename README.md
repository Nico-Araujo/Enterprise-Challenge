# 🏭 Hermes Reply Challenge - Sistema de Monitoramento Industrial


## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/juliano-romeiro-rodrigues/">Juliano Romeiro Rodrigues</a>
- <a href="https://www.linkedin.com/in/nicolas--araujo/">Nicolas Antonio Silva Araujo</a> 
- <a href="https://www.linkedin.com/in/vitoria-bagatin-31ba88266/">Vitória Pereira Bagatin</a> 
<br><br>

## 📋 Sobre o Projeto
Sistema completo de monitoramento industrial 4.0 que integra sensores IoT, machine learning e dashboard em tempo real para predição de falhas e gestão de ativos. Desenvolvido como solução para o desafio Hermes Reply de digitalização industrial.

## 🎯 Objetivos
- ✅ **Objetivo 1**:
- ✅ Pipeline End-to-End: Integração completa desde sensores ESP32 até dashboard com ML
- ✅ Detecção Inteligente: Machine Learning para identificação de anomalias e padrões
- ✅ Alertas Proativos: Sistema de notificações baseado em thresholds e modelos preditivos
- ✅ Visualização em Tempo Real: Dashboard interativo para monitoramento contínuo
- ✅ Gestão de Manutenção: Integração com ordens de serviço baseadas em alertas

## 🏗️ Arquitetura do Sistema
- Sensores ESP32 → Coleta de Dados → Banco de Dados → Machine Learning → Dashboard → Alertas

### 📌 Principais Entidades

## Componentes Principais

| Componente | Tecnologia | Função |
|---|---|---|
| **Coleta** | `ESP32` + Sensores | Captura dados de **temperatura**, **vibração** e **distância** |
| **Banco** | `PostgreSQL`/`SQLite` | Armazena leituras, alertas e ordens de manutenção |
| **ML** | `Scikit-learn` | Detecção de **anomalias** e classificação de alertas |
| **Dashboard** | `Streamlit` + `Plotly` | **Visualização em tempo real** e gestão |

### 🔗 Hierarquia e Relacionamentos
- Cada **Ativo** pertence a um **Tipo de Ativo**  
- Cada **Sensor** está ligado a um **Ativo** e a um **Modelo de Sensor**  
- Cada **Leitura** está associada a um **Sensor**  
- **Alertas** são gerados por leituras fora do padrão em ativos  
- **Ordens de Manutenção** estão vinculadas a alertas e a usuários responsáveis

### 📂 Arquivos Disponíveis no Repositório
 -

### Vídeo de Demonstração
🔗 Clique [AQUI](youtube.com) para ser redirecionado ao vídeo no YouTube.

## 🤖 Sistema de Machine Learning
### Metodologia:
1. Pré-processamento: Limpeza e transformação dos dados dos sensores
2. Engenharia de Features: Tendências, médias móveis e features temporais
3. Detecção de Anomalias: Isolation Forest para padrões anômalos
4. Classificação: Random Forest para estados de alerta (NORMAL, ALERTA, CRÍTICO)
5. Clusterização: KMeans para identificação de padrões de operação

## 🎯 KPIs e Funcionalidades do Dashboard

### ✅ KPIs do Dashboard

* **Monitoramento Contínuo:** Acompanhamento 24/7 dos dados dos sensores.
* **Alertas Automáticos:** Geração de notificações baseadas em *thresholds* (limiares) predefinidos.
* **Visualização Interativa:** Gráficos dinâmicos em tempo real utilizando **Plotly**.
* **Gestão de Alertas:** Interface de controle para técnicos e operadores.

### 🎨 Dashboard Streamlit - Funcionalidades Implementadas
O dashboard foi desenvolvido utilizando **Streamlit** e oferece as seguintes funcionalidades principais:

* **📊 Visão Geral:** Exibição dos **KPIs** (Key Performance Indicators) mais importantes do sistema em tempo real.
* **📈 Série Temporal:** Visualização da evolução histórica das leituras dos sensores, com indicação dos *thresholds* configurados.
* **🔍 Análise de Correlação:** Estudo da relação e dependência entre as diferentes variáveis coletadas.
* **🚨 Sistema de Alertas:** Notificações classificadas e categorizadas por **severidade**.
* **🤖 Performance ML:** Métricas de desempenho dos modelos de *Machine Learning* treinados.

## 📋 Conclusões
---

### 🏭 Impacto Industrial
O sistema implementado gera valor direto para a operação industrial:
* **Redução de Paradas:** A detecção precoce de anomalias evita falhas catastróficas e o *downtime* não planejado.
* **Manutenção Preditiva:** Intervenções são realizadas com base em *insights* de **dados reais** e não em cronogramas fixos.
* **Otimização de Recursos:** Permite a alocação eficiente e precisa das equipes de manutenção, reduzindo custos.
* **Conformidade:** Mantém um registro completo das leituras e intervenções para fins de **auditoria**.

### 🔧 Technical Takeaways
As lições técnicas e a robustez da solução incluem:
* **Arquitetura Escalável:** O *pipeline* modular e desacoplado permite fácil expansão e adição de novos ativos.
* **ML em Produção:** Sucesso na operação de modelos de *Machine Learning* (**Scikit-learn**) em um ambiente real.
* **IoT Integration:** Utilização de protocolos padronizados para integração flexível de diversos tipos de **sensores (ESP32)**.
* **Cloud Ready:** Arquitetura desenhada para um **deploy** simplificado em plataformas de nuvem.

---

**Challenge**: Hermes Reply - Digitalização Industrial  
**Fase**: 5 - Machine Learning e Computação em Nuvem  
**Data**: Setembro 2025
