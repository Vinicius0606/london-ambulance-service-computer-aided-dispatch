-- SistemaAmbulancia | criação do banco e carga inicial para MySQL 8.0.16 ou superior
-- Execute uma vez em um banco vazio. Os quatro primeiros INSERTs usam IDs fixos.
-- No arquivo SistemaAmbulancia/.env, use DB_NAME=sistema_ambulancia.
-- O código lê nomes de tabelas em minúsculas e grava com iniciais maiúsculas.
-- Use uma instância que ignore maiúsculas nos nomes das tabelas, como no padrão do MySQL no Windows.

CREATE DATABASE IF NOT EXISTS `sistema_ambulancia`
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `sistema_ambulancia`;
SET NAMES utf8mb4;

CREATE TABLE endereco (
    ID_endereco BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    CEP VARCHAR(8) NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(32) NULL,
    bairro VARCHAR(255) NULL,
    cidade VARCHAR(255) NOT NULL,
    estado VARCHAR(255) NOT NULL,
    complemento TEXT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    PRIMARY KEY (ID_endereco),
    CONSTRAINT ck_endereco_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT ck_endereco_longitude CHECK (longitude BETWEEN -180 AND 180)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ambulancia (
    ID_ambulancia BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    placa VARCHAR(7) NOT NULL,
    status VARCHAR(50) COLLATE utf8mb4_bin NOT NULL DEFAULT 'Disponivel',
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    PRIMARY KEY (ID_ambulancia),
    CONSTRAINT ck_ambulancia_status CHECK (status IN ('Disponivel', 'Atendendo', 'Indisponivel')),
    CONSTRAINT ck_ambulancia_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT ck_ambulancia_longitude CHECK (longitude BETWEEN -180 AND 180)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chamada (
    ID_chamada BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ID_endereco BIGINT UNSIGNED NOT NULL,
    hora_chamada DATETIME NOT NULL,
    descricao TEXT NOT NULL,
    prioridade TINYINT NOT NULL DEFAULT -1,
    status VARCHAR(50) COLLATE utf8mb4_bin NOT NULL DEFAULT 'Pendente',
    nome_solicitante VARCHAR(255) NULL,
    PRIMARY KEY (ID_chamada),
    CONSTRAINT fk_chamada_endereco FOREIGN KEY (ID_endereco) REFERENCES endereco (ID_endereco),
    CONSTRAINT ck_chamada_prioridade CHECK (prioridade IN (-1, 1, 2, 3, 4)),
    CONSTRAINT ck_chamada_status CHECK (status IN ('Pendente', 'Alocado', 'Finalizado'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE atendimento (
    ID_atendimento BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ID_chamada BIGINT UNSIGNED NOT NULL,
    qtd_ambulancias INT UNSIGNED NULL,
    data_hora_inicio DATETIME NULL,
    data_hora_finalizacao DATETIME NULL,
    PRIMARY KEY (ID_atendimento),
    CONSTRAINT fk_atendimento_chamada FOREIGN KEY (ID_chamada) REFERENCES chamada (ID_chamada)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE atendimento_ambulancia (
    ID_atendimento_ambulancia BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    ID_atendimento BIGINT UNSIGNED NOT NULL,
    ID_ambulancia BIGINT UNSIGNED NOT NULL,
    data_hora_envio DATETIME NULL,
    data_hora_chegada DATETIME NULL,
    status VARCHAR(50) COLLATE utf8mb4_bin NOT NULL DEFAULT 'EmTransito',
    observacoes TEXT NULL,
    PRIMARY KEY (ID_atendimento_ambulancia),
    CONSTRAINT uq_atendimento_ambulancia UNIQUE (ID_atendimento, ID_ambulancia),
    CONSTRAINT fk_despacho_atendimento FOREIGN KEY (ID_atendimento) REFERENCES atendimento (ID_atendimento),
    CONSTRAINT fk_despacho_ambulancia FOREIGN KEY (ID_ambulancia) REFERENCES ambulancia (ID_ambulancia),
    CONSTRAINT ck_despacho_status CHECK (status IN ('EmTransito', 'Retornando', 'Finalizado'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

START TRANSACTION;

INSERT INTO endereco
    (ID_endereco, CEP, logradouro, numero, bairro, cidade, estado, complemento, latitude, longitude)
VALUES
    (1,'72220001','QN 8 Conjunto 2','10','Riacho Fundo I','Brasília','DF','Casa 1',-15.842100,-47.948200),
    (2,'72110002','QNM 18 Conjunto B','22','Ceilândia Sul','Brasília','DF','Casa 2',-15.850300,-47.960800),
    (3,'71930003','QS 3 Conjunto 5','35','Águas Claras','Brasília','DF','Bloco C',-15.838700,-47.982400),
    (4,'71015004','SGAN 912 Bloco C','48','Asa Norte','Brasília','DF','Apto 204',-15.780800,-47.900200),
    (5,'70390005','CLS 210 Bloco B','59','Asa Sul','Brasília','DF','Apto 302',-15.812900,-47.895100),
    (6,'70630006','SHCGN 706 Bloco F','61','Asa Norte','Brasília','DF','Apto 101',-15.789200,-47.892500),
    (7,'70297007','SQS 308 Bloco G','74','Asa Sul','Brasília','DF','Apto 406',-15.820400,-47.901600),
    (8,'71065008','QE 26 Conjunto M','85','Guará II','Brasília','DF','Casa',-15.821800,-47.968700),
    (9,'70680009','SQN 115 Bloco H','96','Asa Norte','Brasília','DF','Apto 503',-15.791500,-47.903800),
    (10,'70670010','SQN 214 Bloco J','101','Asa Norte','Brasília','DF','Apto 602',-15.798300,-47.899400),
    (11,'70650011','SHCES Quadra 907','115','Cruzeiro Novo','Brasília','DF','Casa',-15.804600,-47.944200),
    (12,'70690012','SQNW 110 Bloco K','120','Noroeste','Brasília','DF','Apto 205',-15.794800,-47.927600),
    (13,'71950013','Rua 19 Norte Lote 14','133','Águas Claras','Brasília','DF','Apto 1201',-15.836500,-47.986100),
    (14,'72300014','QR 408 Conjunto 8','145','Samambaia Norte','Brasília','DF','Casa',-15.861200,-47.984500),
    (15,'72610015','Quadra 203 Conjunto 9','156','Recanto das Emas','Brasília','DF','Casa',-15.876400,-47.955200),
    (16,'73010016','Quadra 8 Conjunto D','169','Sobradinho','Brasília','DF','Casa',-15.774900,-47.861300),
    (17,'73310017','Setor Residencial Leste Quadra 4','172','Planaltina','Brasília','DF','Casa',-15.760700,-47.875800),
    (18,'72005018','Rua 4 Chácara 152','188','Vicente Pires','Brasília','DF','Casa',-15.817300,-47.989200),
    (19,'71820019','QN 7 Conjunto 3','199','Riacho Fundo II','Brasília','DF','Casa',-15.865500,-47.971800),
    (20,'71570020','Quadra 12 Conjunto 5','210','Paranoá','Brasília','DF','Casa',-15.789800,-47.843900);

INSERT INTO ambulancia (ID_ambulancia, placa, status, latitude, longitude)
VALUES
    (1,'ABC1234','Disponivel',-15.834400,-47.911496),
    (2,'ABC1235','Atendendo',-15.834400,-47.911496),
    (3,'ABC1236','Disponivel',-15.834400,-47.911496),
    (4,'ABC1237','Atendendo',-15.834400,-47.911496),
    (5,'ABC1238','Atendendo',-15.834400,-47.911496),
    (6,'ABC1239','Disponivel',-15.834400,-47.911496),
    (7,'ABC1240','Disponivel',-15.834400,-47.911496),
    (8,'ABC1241','Atendendo',-15.834400,-47.911496),
    (9,'ABC1242','Disponivel',-15.834400,-47.911496),
    (10,'ABC1243','Disponivel',-15.834400,-47.911496),
    (11,'ABC1244','Atendendo',-15.834400,-47.911496),
    (12,'ABC1245','Disponivel',-15.834400,-47.911496),
    (13,'ABC1246','Disponivel',-15.834400,-47.911496),
    (14,'ABC1247','Disponivel',-15.834400,-47.911496),
    (15,'ABC1248','Disponivel',-15.834400,-47.911496),
    (16,'ABC1249','Disponivel',-15.834400,-47.911496),
    (17,'ABC1250','Disponivel',-15.834400,-47.911496),
    (18,'ABC1251','Disponivel',-15.834400,-47.911496),
    (19,'ABC1252','Disponivel',-15.834400,-47.911496),
    (20,'ABC1253','Disponivel',-15.834400,-47.911496);

-- Os registros de exemplo com prioridade 5 foram convertidos para 4 (Extrema).
INSERT INTO chamada (ID_chamada, ID_endereco, hora_chamada, descricao, prioridade, status, nome_solicitante)
VALUES
    (1,1,'2026-04-01 08:00:00','Dor no peito',4,'Finalizado','Carlos Silva'),
    (2,2,'2026-04-01 08:10:00','Acidente de carro',4,'Alocado','Mariana Souza'),
    (3,3,'2026-04-01 08:20:00','Queda',2,'Finalizado','Rafael Lima'),
    (4,4,'2026-04-01 08:30:00','Desmaio',3,'Alocado','Juliana Costa'),
    (5,5,'2026-04-01 08:40:00','Dificuldade respiratoria',4,'Alocado','Pedro Henrique'),
    (6,6,'2026-04-01 08:50:00','Fratura',3,'Finalizado','Fernanda Alves'),
    (7,7,'2026-04-01 09:00:00','Febre alta',2,'Finalizado','Lucas Martins'),
    (8,8,'2026-04-01 09:10:00','Convulsao',4,'Alocado','Patricia Gomes'),
    (9,9,'2026-04-01 09:20:00','Queimadura',4,'Finalizado','André Rocha'),
    (10,10,'2026-04-01 09:30:00','Hipoglicemia',3,'Finalizado','Camila Ribeiro'),
    (11,11,'2026-04-01 09:40:00','Acidente de moto',4,'Alocado','Bruno Araujo'),
    (12,12,'2026-04-01 09:50:00','Dor abdominal',2,'Finalizado','Larissa Mendes'),
    (13,13,'2026-04-01 10:00:00','Crise de ansiedade',2,'Finalizado','Thiago Barros'),
    (14,14,'2026-04-01 10:10:00','Hemorragia',4,'Finalizado','Aline Nunes'),
    (15,15,'2026-04-01 10:20:00','Parada cardiaca',4,'Finalizado','Renato Freitas'),
    (16,16,'2026-04-01 10:30:00','Queda de escada',3,'Finalizado','Bianca Castro'),
    (17,17,'2026-04-01 10:40:00','Choque eletrico',4,'Finalizado','Eduardo Melo'),
    (18,18,'2026-04-01 10:50:00','Engasgamento',4,'Finalizado','Vanessa Moura'),
    (19,19,'2026-04-01 11:00:00','Corte profundo',3,'Finalizado','Gustavo Pires'),
    (20,20,'2026-04-01 11:10:00','Afogamento',4,'Finalizado','Roberta Dias');

-- Atendimentos em andamento têm data_hora_finalizacao NULL.
INSERT INTO atendimento (ID_atendimento, ID_chamada, qtd_ambulancias, data_hora_inicio, data_hora_finalizacao)
VALUES
    (1,1,1,'2026-04-01 08:01:00','2026-04-01 08:40:00'),
    (2,2,1,'2026-04-01 08:11:00',NULL),
    (3,3,1,'2026-04-01 08:21:00','2026-04-01 09:00:00'),
    (4,4,1,'2026-04-01 08:31:00',NULL),
    (5,5,1,'2026-04-01 08:41:00',NULL),
    (6,6,1,'2026-04-01 08:51:00','2026-04-01 09:20:00'),
    (7,7,1,'2026-04-01 09:01:00','2026-04-01 09:25:00'),
    (8,8,1,'2026-04-01 09:11:00',NULL),
    (9,9,1,'2026-04-01 09:21:00','2026-04-01 09:55:00'),
    (10,10,1,'2026-04-01 09:31:00','2026-04-01 10:10:00'),
    (11,11,1,'2026-04-01 09:41:00',NULL),
    (12,12,1,'2026-04-01 09:51:00','2026-04-01 10:20:00'),
    (13,13,1,'2026-04-01 10:01:00','2026-04-01 10:30:00'),
    (14,14,1,'2026-04-01 10:11:00','2026-04-01 10:48:00'),
    (15,15,1,'2026-04-01 10:21:00','2026-04-01 11:02:00'),
    (16,16,1,'2026-04-01 10:31:00','2026-04-01 11:00:00'),
    (17,17,1,'2026-04-01 10:41:00','2026-04-01 11:12:00'),
    (18,18,1,'2026-04-01 10:51:00','2026-04-01 11:18:00'),
    (19,19,1,'2026-04-01 11:01:00','2026-04-01 11:40:00'),
    (20,20,1,'2026-04-01 11:11:00','2026-04-01 11:55:00');

-- O ID de cada despacho é gerado automaticamente.
INSERT INTO atendimento_ambulancia (ID_atendimento, ID_ambulancia, data_hora_envio, data_hora_chegada, status, observacoes)
VALUES
    (1,1,'2026-04-01 08:02:00','2026-04-01 08:15:00','Finalizado','Paciente estabilizado'),
    (2,2,'2026-04-01 08:12:00',NULL,'EmTransito','Acidente grave'),
    (3,3,'2026-04-01 08:22:00','2026-04-01 08:35:00','Finalizado','Queda leve'),
    (4,4,'2026-04-01 08:32:00',NULL,'EmTransito','Paciente inconsciente'),
    (5,5,'2026-04-01 08:42:00',NULL,'EmTransito','Respiracao dificil'),
    (6,6,'2026-04-01 08:52:00','2026-04-01 09:05:00','Finalizado','Fratura no braço'),
    (7,7,'2026-04-01 09:02:00','2026-04-01 09:15:00','Finalizado','Febre controlada'),
    (8,8,'2026-04-01 09:12:00',NULL,'EmTransito','Convulsao em andamento'),
    (9,9,'2026-04-01 09:22:00','2026-04-01 09:38:00','Finalizado','Queimadura superficial'),
    (10,10,'2026-04-01 09:32:00','2026-04-01 09:45:00','Finalizado','Hipoglicemia revertida'),
    (11,11,'2026-04-01 09:42:00',NULL,'EmTransito','Colisao com motociclista'),
    (12,12,'2026-04-01 09:52:00','2026-04-01 10:08:00','Finalizado','Dor abdominal avaliada'),
    (13,13,'2026-04-01 10:02:00','2026-04-01 10:15:00','Finalizado','Paciente orientado'),
    (14,14,'2026-04-01 10:12:00','2026-04-01 10:29:00','Finalizado','Sangramento controlado'),
    (15,15,'2026-04-01 10:22:00','2026-04-01 10:40:00','Finalizado','Reanimacao iniciada'),
    (16,16,'2026-04-01 10:32:00','2026-04-01 10:50:00','Finalizado','Sem fraturas graves'),
    (17,17,'2026-04-01 10:42:00','2026-04-01 10:58:00','Finalizado','Choque leve'),
    (18,18,'2026-04-01 10:52:00','2026-04-01 11:05:00','Finalizado','Obstrucao removida'),
    (19,19,'2026-04-01 11:02:00','2026-04-01 11:20:00','Finalizado','Curativo realizado'),
    (20,20,'2026-04-01 11:12:00','2026-04-01 11:33:00','Finalizado','Vitima retirada da agua');

COMMIT;

-- A carga inicial deve retornar 20 registros em cada tabela.
SELECT 'endereco' AS tabela, COUNT(*) AS registros FROM endereco
UNION ALL SELECT 'ambulancia', COUNT(*) FROM ambulancia
UNION ALL SELECT 'chamada', COUNT(*) FROM chamada
UNION ALL SELECT 'atendimento', COUNT(*) FROM atendimento
UNION ALL SELECT 'atendimento_ambulancia', COUNT(*) FROM atendimento_ambulancia;
