# 🏭 Hermes Reply Challenge - Sistema de Monitoramento Industrial


## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/juliano-romeiro-rodrigues/">Juliano Romeiro Rodrigues</a>
- <a href="https://www.linkedin.com/in/nicolas--araujo/">Nicolas Antonio Silva Araujo</a> 
- <a href="https://www.linkedin.com/in/vitoria-bagatin-31ba88266/">Vitória Pereira Bagatin</a> 
<br><br>

## 📋 Sobre o Projeto


## 🎯 Objetivos
- ✅ **Objetivo 1**:

## 🏗️ Modelagem do Banco de Dados


### 📌 Principais Entidades

| Entidade | Descrição |
|----------|-----------|
| `TIPOS_ATIVO` | Categorias de equipamentos (Motor, Compressor, Bomba, etc.) |
| `ATIVOS` | Equipamentos físicos instalados na planta |
| `MODELOS_SENSOR` | Catálogo de sensores por fabricante |
| `SENSORES` | Dispositivos IoT conectados a cada ativo |
| `LEITURAS` | Leituras coletadas pelos sensores (alto volume) |
| `USUARIOS` | Operadores e técnicos responsáveis pelo sistema |
| `ALERTAS` | Notificações automáticas baseadas em thresholds |
| `ORDENS_MANUTENCAO` | Ordens de manutenção associadas a alertas |

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

### Metodologia:
- 

### Principais Insights:
- 

## 📋 Conclusões
- 

### ML
- 

---

**Challenge**: Hermes Reply - Digitalização Industrial  
**Fase**: 5 - Machine Learning e Computação em Nuvem  
**Data**: Setembro 2025
