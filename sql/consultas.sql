-- Active: 1749252434297@@127.0.0.1@3306@BANK
SELECT 
t.id AS id,
emisor.nombre AS nombre_emisor,
receptor.nombre AS nombre_receptor,
t.cantidad
FROM transacciones t
JOIN usuarios emisor ON t.id_emisor = emisor.id
JOIN usuarios receptor ON t.id_receptor = receptor.id;
CALL hacer_transferencia(17,20,100);