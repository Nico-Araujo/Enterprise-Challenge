
-- Limpar banco (se necessário)
DROP TABLE IF EXISTS ordens_manutencao CASCADE;
DROP TABLE IF EXISTS alertas CASCADE;
DROP TABLE IF EXISTS leituras CASCADE;
DROP TABLE IF EXISTS sensores CASCADE;
DROP TABLE IF EXISTS ativos CASCADE;
DROP TABLE IF EXISTS modelos_sensor CASCADE;
DROP TABLE IF EXISTS tipos_ativo CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;



-- 1. TABELA: USUARIOS

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY, 
    nome VARCHAR(100) NOT NULL, 
    email VARCHAR(100) UNIQUE NOT NULL, 
    senha_hash VARCHAR(100), 
    cargo VARCHAR(50) 
);


-- 2. TABELA: TIPOS_ATIVO
CREATE TABLE tipos_ativo (
    id_tipo_ativo SERIAL PRIMARY KEY, 
    nome_tipo VARCHAR(100) UNIQUE NOT NULL 
);

-- 3. TABELA: MODELOS_SENSOR
CREATE TABLE modelos_sensor (
    id_modelo SERIAL PRIMARY KEY, 
    nome_modelo VARCHAR(100) NOT NULL, 
    fabricante VARCHAR(100), 
    
    CONSTRAINT nome_modelo_fabricante_unico UNIQUE (nome_modelo, fabricante)
);


-- 4. TABELA: ATIVOS
CREATE TABLE ativos (
    id_ativo SERIAL PRIMARY KEY,
    id_tipo_ativo INTEGER NOT NULL, 
    nome VARCHAR(100) NOT NULL, 
    localizacao VARCHAR(100), 
    dt_instalacao DATE, 
    status VARCHAR(50),
    
    -- Chave estrangeira
    CONSTRAINT fk_tipo_ativo 
        FOREIGN KEY (id_tipo_ativo) 
        REFERENCES tipos_ativo(id_tipo_ativo)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- 5. TABELA: SENSORES
CREATE TABLE sensores (
    id_sensor SERIAL PRIMARY KEY,
    id_ativo INTEGER NOT NULL, 
    id_modelo INTEGER NOT NULL,
    tipo_sensor VARCHAR(50) NOT NULL, 
    status VARCHAR(50),
    
    -- Chaves estrangeiras
    CONSTRAINT fk_ativo_sensor 
        FOREIGN KEY (id_ativo) 
        REFERENCES ativos(id_ativo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_modelo_sensor 
        FOREIGN KEY (id_modelo) 
        REFERENCES modelos_sensor(id_modelo)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- 6. TABELA: LEITURAS
CREATE TABLE leituras (
    id_leitura SERIAL PRIMARY KEY, 
    id_sensor INTEGER NOT NULL, 
    data_hora TIMESTAMP NOT NULL, 
    valor NUMERIC(10, 2) NOT NULL, 
    
    -- Chave estrangeira
    CONSTRAINT fk_sensor_leitura 
        FOREIGN KEY (id_sensor) 
        REFERENCES sensores(id_sensor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- 7. TABELA: ALERTAS 
CREATE TABLE alertas (
    id_alerta SERIAL PRIMARY KEY, 
    id_ativo INTEGER NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    descricao VARCHAR(255),
    severidade VARCHAR(20),
    status VARCHAR(20), 

    -- Chave estrangeira
    CONSTRAINT fk_ativo_alerta 
        FOREIGN KEY (id_ativo) 
        REFERENCES ativos(id_ativo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- 8. TABELA: ORDENS_MANUTENCAO
CREATE TABLE ordens_manutencao (
    id_ordem SERIAL PRIMARY KEY,
    id_alerta INTEGER NOT NULL,
    id_usuario INTEGER, 
    data_criacao DATE DEFAULT CURRENT_DATE,
    data_conclusao DATE, 
    status VARCHAR(50), 
    descricao_servico TEXT, 

    -- Chaves estrangeiras
    CONSTRAINT fk_alerta_ordem 
        FOREIGN KEY (id_alerta) 
        REFERENCES alertas(id_alerta)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_usuario_ordem 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);



-- INSERÇÃO DE DADOS DE EXEMPLO 

-- Inserir usuários
INSERT INTO usuarios (nome, email, cargo, senha_hash) VALUES
('João Silva', 'joao.silva@empresa.com', 'Engenheiro', 'hash123'),
('Maria Santos', 'maria.santos@empresa.com', 'Técnica', 'hash456'),
('Pedro Oliveira', 'pedro.oliveira@empresa.com', 'Supervisor', 'hash789');

-- Inserir tipos de ativo
INSERT INTO tipos_ativo (nome_tipo) VALUES
('Bomba'),
('Motor'),
('Compressor');

-- Inserir modelos de sensor
INSERT INTO modelos_sensor (nome_modelo, fabricante) VALUES
('TempSensor Pro 3000', 'Siemens'),
('VibrationMax V2', 'ABB'),
('PressureGuard Elite', 'Schneider');

-- Inserir ativos
INSERT INTO ativos (nome, id_tipo_ativo, localizacao, dt_instalacao, status) VALUES
('Bomba Principal A1', 1, 'Setor A - Linha 1', '2023-01-15', 'ativo'),
('Motor Secundário B2', 2, 'Setor B - Linha 2', '2023-03-20', 'ativo'),
('Compressor Central C1', 3, 'Setor C - Área Central', '2023-02-10', 'ativo');

-- Inserir sensores
INSERT INTO sensores (id_ativo, id_modelo, tipo_sensor, status) VALUES
(1, 1, 'temperatura', 'ativo'),
(1, 2, 'vibração', 'ativo'),
(2, 1, 'temperatura', 'ativo'),
(3, 3, 'pressão', 'ativo');

-- Inserir leituras
INSERT INTO leituras (id_sensor, data_hora, valor) VALUES
(1, '2025-01-15 10:00:00', 25.5),
(1, '2025-01-15 10:05:00', 26.2),
(2, '2025-01-15 10:00:00', 2.3),
(3, '2025-01-15 10:00:00', 45.1);

-- Inserir alertas 
INSERT INTO alertas (id_ativo, data_hora, descricao, severidade, status) VALUES
(1, CURRENT_TIMESTAMP, 'Temperatura alta detectada na Bomba Principal A1.', 'alta', 'aberto'),
(2, CURRENT_TIMESTAMP, 'Vazamento de óleo detectado no Motor B2.', 'crítica', 'aberto');

-- Inserir ordens de manutenção 
INSERT INTO ordens_manutencao (id_alerta, id_usuario, data_criacao, data_conclusao, status, descricao_servico) VALUES
(1, 1, '2025-01-16', '2025-01-17', 'concluída', 'Resfriamento ajustado para controle de temperatura.'),
(2, 2, '2025-01-16', NULL, 'em_andamento', 'Reparo de vazamento e troca de vedação.');


-- CONSULTAS DE VERIFICAÇÃO


-- Verificar a nova tabela ALERTAS
SELECT * FROM alertas;

-- Verificar ORDENS_MANUTENCAO 
SELECT 
    om.id_ordem, 
    a.descricao AS alerta_origem, 
    u.nome AS responsavel,
    om.status, 
    om.descricao_servico
FROM ordens_manutencao om
JOIN alertas a ON om.id_alerta = a.id_alerta
LEFT JOIN usuarios u ON om.id_usuario = u.id_usuario;

