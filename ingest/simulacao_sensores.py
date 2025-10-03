import csv
import random
import time


# CONFIGURAÇÃO DE SIMULAÇÃO

NUM_LEITURAS = 200  # Total de pontos de tempo a simular
INTERVALO_MS = 1000 # Simula leituras a cada 1000ms (1 segundo)
NOME_ARQUIVO = "leituras_stream.csv"
DELIMITADOR = ";"

# Definição dos sensores e seus limites (baseados no seu código C++)
SENSORES = {
    # ID: (Nome, Faixa_Mín, Faixa_Máx, Faixa_Alerta, Faixa_Crítica)
    1: ("Temperatura (°C)", 20.0, 100.0, 60.0, 80.0),
    2: ("Vibração (g)", 0.1, 3.0, 1.0, 2.0),
    3: ("Distância/Nível (cm)", 5.0, 250.0, 10.0, 5.0), # Crítico é < 5.0 (Dist_Min)
}

# Variáveis globais para simulação de tendência
tendencia_temp = 30.0
tendencia_vib = 0.5
tendencia_dist = 150.0

# FUNÇÕES DE GERAÇÃO DE DADOS


def gerar_leitura_variavel(valor_atual, min_val, max_val, max_delta):
    """Ajusta o valor atual com um pequeno delta aleatório, mantendo-o dentro dos limites."""
    delta = random.uniform(-max_delta, max_delta)
    novo_valor = valor_atual + delta
    
    # Garante que o valor não saia dos limites extremos
    if novo_valor < min_val:
        novo_valor = min_val
    if novo_valor > max_val:
        novo_valor = max_val
        
    return novo_valor

def simular_ponto_no_tempo(leitura_id, tempo_ms):
    """Gera leituras para todos os sensores em um único ponto de tempo."""
    global tendencia_temp, tendencia_vib, tendencia_dist
    
    registros = []
    
    # Iterar sobre cada sensor
    for id_sensor, (nome, min_val, max_val, alerta, critico) in SENSORES.items():
        
        # 1. Ajuste da tendência para gerar série temporal
        if id_sensor == 1: # Temperatura
            # Simula aumento de temperatura de 0.5% a cada leitura (tendência de aquecimento)
            max_delta = 0.8 
            tendencia_temp = gerar_leitura_variavel(tendencia_temp, min_val, max_val, max_delta)
            valor_leitura = round(tendencia_temp, 2)
            
            # Força um pico crítico em 2 momentos da série (para provar o alerta)
            if 50 < leitura_id < 70 or 150 < leitura_id < 170:
                tendencia_temp += 3.0 # Aumenta 3 graus para forçar o CRÍTICO
                valor_leitura = round(tendencia_temp, 2)

        elif id_sensor == 2: # Vibração
            max_delta = 0.1 
            tendencia_vib = gerar_leitura_variavel(tendencia_vib, min_val, max_val, max_delta)
            valor_leitura = round(tendencia_vib, 2)
            
            # Força um pico de vibração crítica
            if 90 < leitura_id < 110:
                 tendencia_vib += 0.5
                 valor_leitura = round(tendencia_vib, 2)
        
        elif id_sensor == 3: # Distância/Nível
            max_delta = 5.0
            tendencia_dist = gerar_leitura_variavel(tendencia_dist, min_val, max_val, max_delta)
            valor_leitura = round(tendencia_dist, 2)
        
        # 2. Adicionar o registro no formato Longo (CSV)
        registros.append({
            'id_local': leitura_id,
            'data_hora_ms': tempo_ms,
            'id_sensor': id_sensor,
            'valor': valor_leitura
        })
        
    return registros


# EXECUÇÃO E ESCRITA DO ARQUIVO CSV

def main():
    """Gera o arquivo CSV de simulação."""
    
    print(f"Iniciando simulação de {NUM_LEITURAS} pontos de tempo...")
    
    # Define os campos do cabeçalho
    campos = ['id_local', 'data_hora_ms', 'id_sensor', 'valor']
    
    with open(NOME_ARQUIVO, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=DELIMITADOR)
        
        # Escreve o cabeçalho
        escritor.writeheader()
        
        tempo_base = int(time.time() * 1000) # Tempo inicial em milissegundos
        
        for i in range(1, NUM_LEITURAS + 1):
            tempo_atual_ms = tempo_base + i * INTERVALO_MS
            
            registros = simular_ponto_no_tempo(i, tempo_atual_ms)
            
            # Escreve os dados (uma linha para cada sensor)
            escritor.writerows(registros)
            
    print(f"Simulação concluída! Arquivo gerado em: {NOME_ARQUIVO}")
    print(f"Total de linhas geradas: {NUM_LEITURAS * len(SENSORES)}")

if __name__ == "__main__":
    main()