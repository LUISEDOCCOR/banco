import streamlit as st
import pandas as pd
from db import hacer_transaccion, obtener_usuarios, crear_usuario, obtener_transacciones, hacer_transaccion_procedure, init_database

init_database()

st.title("🏫 Banco")
st.sidebar.title("Navegación")

opciones = ["Usuarios", "Crear Usuario", "Hacer transferencia", "Historial"]
emojis = "🪪 📤 📦 📕".split(" ")

pagina = st.sidebar.radio("Seleccióna una página", opciones)

st.subheader(f"{emojis[opciones.index(pagina)]} {pagina}")

#Usuarios
if pagina == opciones[0]:
    usuarios = obtener_usuarios()
    df = pd.DataFrame(usuarios, columns=["ID", "Nombre", "Saldo"])
    st.dataframe(df)
    top_5 = df.sort_values(by="Saldo", ascending=False).head(5)
    st.bar_chart(top_5.set_index("Nombre")["Saldo"])

#Crear Usuario
if pagina == opciones[1]:
    with st.form("form_crear_usuario", clear_on_submit=True):
        nombre = st.text_input("Nombre: ")
        saldo = st.number_input("Saldo", min_value=0.0, step=0.1)
        submit = st.form_submit_button("➕ Crear")

        if submit:
            if nombre.strip() == "":
                st.warning("El nombre no puede estar vacio")
            else:
                try:
                    crear_usuario(nombre, saldo)
                    st.success(f"Creado correctamente el usuario: {nombre}")
                except Exception as e:
                    st.error(f"Hubo un error {e}")

#Hacer transferencia
if pagina == opciones[2]:
    with st.form("form_transaccion", clear_on_submit=True):
        usuarios = obtener_usuarios()
        emisor = st.selectbox(
            "Emisor: ",
            usuarios,
            format_func=lambda usuario: f"{usuario[1]} - Saldo: ${usuario[2]}"
        )
        receptor = st.selectbox(
            "Receptor: ",
            usuarios,
            format_func=lambda usuario: f"{usuario[1]} - Saldo: ${usuario[2]}"
        )
        monto = st.number_input("Monto:", min_value=0.01, step=0.01)
        usar_sql_procedure = st.toggle("Usar sql procedure")
        submit = st.form_submit_button("Transferir")

        if submit:
            if not emisor or not receptor:
                st.warning("Selecciona a un receptor y emisor")
            elif emisor[0] == receptor[0]:
                st.warning("El emisor y el receptor no pueden ser la misma persona")
            elif monto > emisor[2]:
                st.warning("Fondos insuficientes")
            else:
                if usar_sql_procedure:
                    if hacer_transaccion_procedure(emisor[0], receptor[0], monto):
                        st.success("Realizado correctamente")
                    else:
                        st.error("Hubo un error")
                else:
                    if hacer_transaccion(emisor[0], receptor[0], monto):
                        st.success("Realizado correctamente")
                    else:
                        st.error("Hubo un error")

#Historial
if pagina == opciones[3]:
    transacciones = obtener_transacciones()
    df = pd.DataFrame(transacciones, columns=["ID", "Emisor", "Receptor", "Monto"])
    st.dataframe(df)