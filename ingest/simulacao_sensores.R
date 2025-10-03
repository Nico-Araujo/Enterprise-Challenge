# Projeto de Simulação de Sensores (ESP32) em R

# Instale o pacote ggplot2 se necessário:
# install.packages("ggplot2")
# Instale o pacote dplyr para manipular e filtrar o formato longo:
# install.packages("dplyr") 

library(ggplot2)
library(dplyr) # Necessário para filtrar o formato de dados longo

# Leitura do arquivo CSV que está na mesma pasta do script
# ATENÇÃO: O CSV do Monitor Serial usa ';' como separador e '.' como decimal.
dados_long <- read.csv("leituras_stream.csv", header = TRUE, sep = ";", dec = ".") 

# Renomear 'data_hora_ms' para 'tempo'
dados_long <- dados_long %>%
  rename(tempo = data_hora_ms)

# =======================================================
# GRÁFICO DE TEMPERATURA (ID do Sensor = 1)
# =======================================================
dados_temp <- dados_long %>% filter(id_sensor == 1)

# O eixo Y agora usa a coluna 'valor'
ggplot(dados_temp, aes(x = tempo, y = valor)) +
  geom_line(color = "blue") +
  geom_hline(yintercept = 60, color = "orange", linetype = "dashed") +
  geom_hline(yintercept = 90, color = "red", linetype = "dashed") +
  labs(title = "Monitoramento de Temperatura",
       x = "Tempo", y = "Temperatura (°C)") +
  theme_minimal()

# =======================================================
# GRÁFICO DE VIBRAÇÃO (ID do Sensor = 2)
# =======================================================
dados_vib <- dados_long %>% filter(id_sensor == 2)

# O eixo Y agora usa a coluna 'valor'
ggplot(dados_vib, aes(x = tempo, y = valor)) +
  geom_line(color = "darkgreen") +
  geom_hline(yintercept = 1.0, color = "orange", linetype = "dashed") +
  geom_hline(yintercept = 2.0, color = "red", linetype = "dashed") +
  labs(title = "Monitoramento de Vibração",
       x = "Tempo", y = "Vibração (g)") +
  theme_minimal()

# =======================================================
# GRÁFICO DE DISTÂNCIA (ID do Sensor = 3)
# =======================================================
dados_dist <- dados_long %>% filter(id_sensor == 3)

# O eixo Y agora usa a coluna 'valor'
ggplot(dados_dist, aes(x = tempo, y = valor)) +
  geom_line(color = "purple") +
  geom_hline(yintercept = 5, color = "red", linetype = "dotted") +
  geom_hline(yintercept = 250, color = "orange", linetype = "dashed") +
  labs(title = "Monitoramento de Distância com HC-SR04",
       x = "Tempo", y = "Distância (cm)") +
  theme_minimal()