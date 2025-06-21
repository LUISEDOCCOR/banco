from sqlalchemy import create_engine, text
from faker import Faker
from random import uniform
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DB_URL")
engine = create_engine(f"mysql+pymysql://{db_url}")
faker = Faker()

def init_database ():
    with engine.connect() as conn:
        #Tabla usuarios
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100),
                saldo DOUBLE(10, 2)
            );
        """))
        #Tabla transacciones
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS transacciones (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_emisor INT,
                id_receptor INT,
                cantidad DOUBLE(10, 2),
                FOREIGN KEY (id_emisor) REFERENCES usuarios(id),
                FOREIGN KEY (id_receptor) REFERENCES usuarios(id)
            );
        """))

def obtener_usuario_by_id(id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM usuarios WHERE id = :id")
        result = conn.execute(query, {"id": id})
        datos = result.fetchone()
        return datos

def obtener_usuarios():
    with engine.connect() as conn:
        query = text("SELECT * FROM usuarios")
        result = conn.execute(query)
        datos = result.fetchall()
        return datos

def crear_usuario(nombre: str, saldo: float):
    with engine.connect() as conn:
        query = text("INSERT INTO usuarios (nombre, saldo) VALUES (:nombre, :saldo)")
        conn.execute(query, {"nombre": nombre, "saldo": saldo})
        conn.commit()

def crear_usuarios_random(x: int):
    for _ in range(x):
        nombre = faker.name()
        saldo = round(uniform(0, 10000), 2)
        crear_usuario(nombre, saldo)

def hacer_transaccion (id_emisor: int, id_receptor: int, monto: float):
    with engine.connect() as conn:
        trans = conn.begin() #Iniciar transaccion (sql)
        try:
            query = text("SELECT saldo FROM usuarios WHERE id = :id")
            result = conn.execute(query, {"id": id_emisor})
            saldo_emisor = result.scalar_one()

            if saldo_emisor < monto:
                return False

            query = text("UPDATE usuarios SET saldo = saldo - :monto WHERE id = :id")
            conn.execute(query, {"monto": monto, "id": id_emisor})

            query = text("UPDATE usuarios SET saldo = saldo + :monto WHERE id = :id")
            conn.execute(query, {"monto": monto, "id": id_receptor})

            query = text("""
                INSERT INTO transacciones
                (id_emisor, id_receptor, cantidad)
                VALUES (:id_emisor, :id_receptor, :cantidad)
            """)
            conn.execute(query, {"id_emisor": id_emisor, "id_receptor": id_receptor, "cantidad": monto})

            trans.commit()
            return True
        except Exception as e:
            trans.rollback()
            print(e)
            return False

def obtener_transacciones ():
    with engine.connect() as conn:
        query = text("""
            SELECT 
            t.id AS id,
            emisor.nombre AS nombre_emisor,
            receptor.nombre AS nombre_receptor,
            t.cantidad
            FROM transacciones t
            JOIN usuarios emisor ON t.id_emisor = emisor.id
            JOIN usuarios receptor ON t.id_receptor = receptor.id
        """)
        result = conn.execute(query)
        transacciones = result.fetchall()
        return transacciones

def hacer_transaccion_procedure(id_emisor: int, id_receptor: int, monto: float):
    with engine.connect() as conn:
        try:
            query = text("CALL hacer_transferencia(:id_emisor , :id_receptor , :monto)")
            conn.execute(query,{"id_emisor": id_emisor, "id_receptor": id_receptor, "monto": monto})
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False