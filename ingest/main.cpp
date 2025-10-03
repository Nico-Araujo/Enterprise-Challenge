#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <MPU6050.h>
#include <WiFi.h>


// DEFINIÇÕES E PINAGEM 

#define ONE_WIRE_BUS 4      // Pino do sensor DS18B20 (GPIO4)
#define TRIG_PIN 5          // Pino Trig do HC-SR04 (GPIO5)
#define ECHO_PIN 18         // Pino Echo do HC-SR04 (GPIO18)
#define RELAY_PIN 19        // Pino para controle do relé (GPIO19)
#define BUZZER_PIN 23       // Pino do buzzer (GPIO23)
#define LED_GREEN 21        // Pino do LED verde (GPIO21)
#define LED_YELLOW 22       // Pino do LED amarelo (GPIO22)
#define LED_RED 25          // Pino do LED vermelho (GPIO25)
#define MPU_SDA 15          // Pino SDA secundário para MPU6050 (GPIO15)
#define MPU_SCL 16          // Pino SCL secundário para MPU6050 (GPIO16)

// Limites de operação (retidos do código original)
#define TEMP_WARNING 60.0    // Temperatura de alerta (ºC)
#define TEMP_CRITICAL 80.0   // Temperatura crítica (ºC)
#define TEMP_SHUTDOWN 90.0   // Temperatura para desligamento (ºC)
#define VIB_WARNING 1.0      // Vibração de alerta (g)
#define VIB_CRITICAL 2.0     // Vibração crítica (g)
#define DIST_MIN 5.0         // Distância mínima (cm)
#define DIST_MAX 250.0       // Distância máxima (cm)
#define DIST_WARNING_LOW 10.0  // Distância baixa de alerta (cm)
#define DIST_WARNING_HIGH 200.0 // Distância alta de alerta (cm)

// Objetos dos sensores
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
MPU6050 mpu;

// Variáveis de estado
bool systemNormal = true;
bool systemWarning = false;
bool systemCritical = false;

// Variáveis de leitura dos sensores
float temperature = 0.0;
float vibration = 0.0;
float distance = 0.0;

// Variável para rastrear a ordem da leitura local (Índice para o CSV)
static long leitura_id_local = 0;

// Protótipos das funções
float measureDistance();
void updateStatusIndicators();
void logDataToSerial(long id_local, long time_ms, int sensor_id, float valor);


void setup() {
  Serial.begin(115200);

  // Conectando ao WIFI (mantido do código original)
  Serial.print("Conectando-se ao Wi-Fi");
  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println(" Conectado!");

  // Inicializa os pinos e sensores (mantido do código original)
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(RELAY_PIN, HIGH);
  sensors.begin();
  Wire.begin(MPU_SDA, MPU_SCL);
  mpu.initialize();
  
  if(!mpu.testConnection()) {
    Serial.println("ERRO: MPU6050 não conectado! Verifique a fiação.");
  }
  
  Serial.println("Sistema inicializado. Iniciando monitoramento...");
  
  // =======================================================
  // CABEÇALHO CSV PARA O BANCO DE DADOS (CRÍTICO PARA O REQUISITO)
  // =======================================================
  // Colunas: ID_Local, Data_MS, ID_Sensor_DB, Valor
  Serial.println("id_local;data_hora_ms;id_sensor;valor");
}

void loop() {
  // Reinicia os estados
  systemNormal = true;
  systemWarning = false;
  systemCritical = false;
  
  // 1. Monitoramento de Temperatura (DS18B20)
  sensors.requestTemperatures();
  temperature = sensors.getTempCByIndex(0);
  
  if (temperature == DEVICE_DISCONNECTED_C) {
    Serial.println("Falha ao ler o sensor de temperatura!");
  } else {
    // Lógica de alerta original
    if (temperature > TEMP_CRITICAL || temperature >= TEMP_SHUTDOWN) {
      systemCritical = true;
      if (temperature >= TEMP_SHUTDOWN) {
        digitalWrite(RELAY_PIN, LOW);
        Serial.println("EMERGÊNCIA: Equipamento desligado por superaquecimento!");
      }
    } else if (temperature > TEMP_WARNING) {
      systemWarning = true;
    }
  }
  
  // 2. Monitoramento de Vibração (MPU6050)
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  float vibrationX = ax / 16384.0;
  float vibrationY = ay / 16384.0;
  float vibrationZ = az / 16384.0;
  vibration = sqrt(vibrationX*vibrationX + vibrationY*vibrationY + vibrationZ*vibrationZ);
  
  // Lógica de alerta original
  if (vibration > VIB_CRITICAL) {
    systemCritical = true;
    digitalWrite(RELAY_PIN, LOW); 
  } else if (vibration > VIB_WARNING) {
    systemWarning = true;
  }
  
  // 3. Monitoramento de Distância (HC-SR04)
  distance = measureDistance();
  
  // Lógica de alerta original
  if (distance < DIST_MIN || distance > DIST_MAX) {
    systemCritical = true;
  } else if (distance < DIST_WARNING_LOW || distance > DIST_WARNING_HIGH) {
    systemWarning = true;
  }
  
  // =======================================================
  // GERAÇÃO DO STREAM CSV PARA BANCO DE DADOS
  // =======================================================
  leitura_id_local++;
  long data_hora_ms = millis(); 
  
  // Log 1: Temperatura (Mapeado para ID_SENSOR = 1)
  logDataToSerial(leitura_id_local, data_hora_ms, 1, temperature);
  
  // Log 2: Vibração (Mapeado para ID_SENSOR = 2)
  logDataToSerial(leitura_id_local, data_hora_ms, 2, vibration);
  
  // Log 3: Distância/Nível (Mapeado para ID_SENSOR = 3)
  logDataToSerial(leitura_id_local, data_hora_ms, 3, distance);

  // Impressões de estado (Opcional, mas útil para ver o status no Monitor)
  Serial.print("ESTADO: ");
  if (systemCritical) Serial.println("CRÍTICO");
  else if (systemWarning) Serial.println("ALERTA");
  else Serial.println("NORMAL");
  
  // Controle dos LEDs e buzzer
  updateStatusIndicators();
  
  delay(1000); // Aguarda 1 segundo entre as leituras (mantido do original)
}

// =======================================================
// FUNÇÕES AUXILIARES (RETIDAS DO CÓDIGO ORIGINAL)
// =======================================================

float measureDistance() {
  // Envia pulso de 10us no pino Trig
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // Mede o tempo de resposta no pino Echo
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calcula a distância (cm)
  float distance = duration * 0.034 / 2;
  
  return distance;
}

void updateStatusIndicators() {
  // Desliga todos os LEDs primeiro
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  noTone(BUZZER_PIN);
  digitalWrite(BUZZER_PIN, LOW);
  
  if (systemCritical) {
    // Estado crítico - LED vermelho e buzzer
    digitalWrite(LED_RED, HIGH);
    tone(BUZZER_PIN, 1000); // Buzzer ativo (1000Hz)
  } else if (systemWarning) {
    // Estado de alerta - LED amarelo
    digitalWrite(LED_YELLOW, HIGH);
  } else {
    // Estado normal - LED verde
    digitalWrite(LED_GREEN, HIGH);
  }
}

// =======================================================
// NOVA FUNÇÃO: Formatar Dados CSV
// =======================================================
void logDataToSerial(long id_local, long time_ms, int sensor_id, float valor) {
  // id_local;data_hora_ms;id_sensor;valor
  Serial.print(id_local);
  Serial.print(";");
  Serial.print(time_ms); 
  Serial.print(";");
  Serial.print(sensor_id); 
  Serial.print(";");
  Serial.println(valor, 2); // Imprime o valor com 2 casas decimais
}