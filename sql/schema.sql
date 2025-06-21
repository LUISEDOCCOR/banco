CREATE DATABASE BANK;
USE BANK;
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    saldo DOUBLE(10, 2)
);
CREATE TABLE IF NOT EXISTS transacciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_emisor INT,
    id_receptor INT,
    cantidad DOUBLE(10, 2),
    FOREIGN KEY (id_emisor) REFERENCES usuarios(id),
    FOREIGN KEY (id_receptor) REFERENCES usuarios(id)
);
