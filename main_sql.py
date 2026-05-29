# -------- CONEXIÓN ORACLE --------
import oracledb
import pandas as pd
import streamlit as st
from datetime import date

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_26")

conn = oracledb.connect(
    user="cristian",
    password="Cenicient4!!",
    dsn="adbg07_low"
)

def consultar(sql):
    return pd.read_sql(sql, conn)



# -------- INTERFAZ --------
st.set_page_config(page_title="BudAppest 🏨", layout="wide")
st.title("Hotel Budapest 🏨")
st.write("Sistema de reservas conectado a Oracle")

st.sidebar.header("Menú")

pagina = st.sidebar.radio("Seleccione una opcion", [
    "🛏️ Habitaciones disponibles",
    "🔍 Consultar reservas",
    "📆 Registrar nueva reserva",
    "💵 Registrar pago"
])

col_1, col_2 = st.columns(2)

with col_1:
    st.write("Sistema de gestión de reservas BudAppest")

with col_2:
    st.write(f"Sección activa: **{pagina}**")

st.divider()

# -------- 1. HABITACIONES DISPONIBLES --------
if pagina == "🛏️ Habitaciones disponibles":
    st.subheader("🛏️ Habitaciones disponibles")

    sql = """
    SELECT num_habitacion, tipo, precio_noche
    FROM ht_habitaciones
    WHERE estado = 'DISPONIBLE'
    """

    disponibles = consultar(sql)

    st.write(f"Total habitaciones disponibles: **{len(disponibles)}**")

    st.dataframe(disponibles.rename(columns={
        "num_habitacion": "Número",
        "tipo": "Tipo",
        "precio_noche": "Precio por noche"
    }), use_container_width=True, hide_index=True)


# -------- 2. CONSULTAR RESERVAS --------
elif pagina == "🔍 Consultar reservas":
    st.subheader("🔍 Reservas registradas")

    estado = st.selectbox("Filtrar por estado", ["ACTIVA", "PAGO", "NO LLEGO", "CANCELADA"])

    sql = f"""
    SELECT 
        r.reserva_id,
        h.nombre,
        hb.num_habitacion,
        r.fecha_ingreso,
        r.fecha_salida,
        r.monto_total,
        r.estado
    FROM ht_reservas r
    JOIN ht_huespedes h ON r.huesped_id = h.huesped_id
    JOIN ht_habitaciones hb ON r.habitacion_id = hb.habitacion_id
    WHERE r.estado = '{estado}'
    ORDER BY r.reserva_id"""

    reservas = consultar(sql)

    st.write(f"Reservas encontradas: **{len(reservas)}**")

    st.dataframe(reservas.rename(columns={
        "reserva_id": "ID",
        "nombre": "Huésped",
        "num_habitacion": "Habitación",
        "fecha_ingreso": "Entrada",
        "fecha_salida": "Salida",
        "monto_total": "Total",
        "estado": "Estado"
    }), use_container_width=True, hide_index=True)


# -------- 3. REGISTRAR NUEVA RESERVA --------
elif pagina == "📆 Registrar nueva reserva":
    st.subheader("📆 Nueva reserva")

    sql = """
    SELECT habitacion_id, num_habitacion, tipo, precio_noche
    FROM ht_habitaciones
    WHERE estado = 'DISPONIBLE'
    """

    disponibles = consultar(sql)

    opciones_hab = disponibles["NUM_HABITACION"] + "-" + disponibles["TIPO"] + " ($" + disponibles["PRECIO_NOCHE"].astype(str) + ")"

    col_3, col_4 = st.columns(2)

    with col_3:
        num_doc = st.text_input("Número de documento")
        habitacion = st.selectbox("Habitación", opciones_hab.tolist())
        fecha_entrada = st.date_input("Fecha de entrada", value=date.today())

    with col_4:
        nombre = st.text_input("Nombre")
        canal = st.selectbox("Canal", ["TRANSFERENCIA", "PSE", "TC"])
        fecha_salida = st.date_input("Fecha de salida", value=date.today())

        hab_sel = disponibles[opciones_hab == habitacion]

        if not hab_sel.empty:
            precio = int(hab_sel["PRECIO_NOCHE"].values[0])
            noches = max((fecha_salida - fecha_entrada).days, 0)
            # Para evitar valores negativos
            noches = max(noches, 0)
            st.info(f"{noches} noches x \\${precio} = \\${noches*precio: ,}")
            if st.button("Registrar reserva", type="primary"):
                st.warning("Complete el nombre y el número de documento")
            elif fecha_salida <= fecha_entrada:
                st.warning("La fecha de salida debe ser posterior que la fecha de entrada")
            else:
                # AQUI SE REGISTRA CON ORACLE
                st.success(f"Reserva registrada a nombre de {nombre} por {noches} noches, por un valor total de \\${noches*precio: ,}")

# -------- 4. REGISTRAR PAGO --------
elif pagina == "💵 Registrar pago":
    st.subheader("💵 Registrar pago")

    sql = """
    SELECT 
        r.reserva_id,
        h.nombre,
        hb.num_habitacion,
        r.monto_total - NVL(SUM(p.monto_pago),0) AS saldo_pendiente
    FROM ht_reservas r
    JOIN ht_huespedes h ON r.huesped_id = h.huesped_id
    JOIN ht_habitaciones hb ON r.habitacion_id = hb.habitacion_id
    LEFT JOIN ht_pagos p ON r.reserva_id = p.reserva_id
    WHERE r.estado = 'ACTIVA'
    GROUP BY r.reserva_id, h.nombre, hb.num_habitacion, r.monto_total
    HAVING r.monto_total - NVL(SUM(p.monto_pago),0) > 0
    """

    pagos = consultar(sql)

    if pagos.empty:
        st.info("No hay saldos pendientes")

    else:
        etiquetas = pagos["NOMBRE"] + " — Hab. " + pagos["NUM_HABITACION"]
        reserva_sel = st.selectbox("Reserva", etiquetas.tolist())

        fila = pagos[etiquetas == reserva_sel].iloc[0]
        saldo = float(fila["SALDO_PENDIENTE"])

        st.write(f"Saldo pendiente: **${saldo:,.0f}**")

        col_1, col_2 = st.columns(2)
        with col_1:
            monto = st.number_input("Monto del pago ($)", min_value=1000.0, max_value=saldo, value=saldo, step=10000.0)
        with col_2:
            medio = st.selectbox("Medio de pago", ["EFECTIVO", "TARJETA_CREDITO", "TRANSFERENCIA", "PSE"])

        if st.button("Registrar pago", type="primary"):
            st.success(f"Pago de ${monto:,.0f} registrado por {medio}.")
