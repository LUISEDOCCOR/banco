DELIMITER //
CREATE PROCEDURE IF NOT EXISTS hacer_transferencia (IN p_id_emisor INT, IN p_id_receptor INT, IN p_monto DOUBLE)
BEGIN
    DECLARE saldo_emisor DOUBLE;
    DECLARE saldo_receptor DOUBLE;
    START TRANSACTION;
        SELECT saldo INTO saldo_emisor FROM usuarios WHERE id = p_id_emisor FOR UPDATE;
        SELECT saldo INTO saldo_receptor FROM usuarios WHERE id = p_id_receptor FOR UPDATE;
        IF saldo_emisor >= p_monto THEN
            UPDATE usuarios SET saldo = saldo_emisor - p_monto WHERE id = p_id_emisor;
            UPDATE usuarios SET saldo = saldo_receptor + p_monto WHERE id = p_id_receptor;
            INSERT INTO transacciones (id_emisor, id_receptor, cantidad) VALUES (p_id_emisor, p_id_receptor, p_monto);
            COMMIT;
        ELSE
            ROLLBACK;
        END IF;
END //
DELIMITER ;