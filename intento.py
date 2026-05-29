# Importamos librerías
import streamlit as st
import pandas as pd
import numpy as np
import oracledb
from datetime import date


# -----------------------------------------------------------------------------
# ----------- Función para conectar e ingresar consultas SQL --------
# -----------------------------------------------------------------------------

def conectar():
    oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_26")
    return oracledb.connect(
        user="andrea",
        password="Cenicient4!!",
        dsn="adbg07_low"
    )


def consultar(sql):
    conn = conectar()
    return pd.read_sql(sql, conn)


# ---------------------------------------------------------------------------
# ----------- Título y descripción ---------------------------------------
# ---------------------------------------------------------------------------

st.set_page_config(page_title='BudAppest 🏩', layout='wide')
st.title('Hotel Budapest')
st.write('Esta aplicación gestiona el sistema de reservas del Hotel Budapest')

# ----------------------------------------------------------------------------
# ----------- Menú lateral ------------------------------------------------
# ----------------------------------------------------------------------------

st.sidebar.header('Menú')
pagina = st.sidebar.radio(
    'Seleccione una opcion',
    [
        '🛌 Habitaciones disponibles',
        '🔍 Consultar reservas',
        '📅 Registrar nueva reserva',
        '💵 Registrar pago'
    ]
)

col_1, col_2 = st.columns(2)
with col_1:
    st.write('Sistema de gestión de reservas BudApest')
with col_2:
    st.write(f'Sección activa: **{pagina}**')

st.divider()

# ----------------------------------------------------------------------------
# ----------- 1. HABITACIONES DISPONIBLES -----------------------
# ----------------------------------------------------------------------------

if pagina == '🛌 Habitaciones disponibles':
    st.subheader('🛌 Habitaciones disponibles')

    disponibles = consultar("""
                            select num_habitacion,
                                   tipo,
                                   precio_noche
                            from ht_habitaciones
                            where estado = 'DISPONIBLE'
                            order by num_habitacion
                            """)

    st.write(f'Total de habitaciones disponibles: **{len(disponibles)}**')

    st.dataframe(
        disponibles.rename(columns={
            'num_habitacion': 'Número',
            'tipo': 'Tipo',
            'precio_noche': 'Precio por noche'
        }),
        use_container_width=True,
        hide_index=True
    )

# ----------------------------------------------------------------------
# ----------- 2. CONSULTAR RESERVAS -------------------------
# ----------------------------------------------------------------------

elif pagina == '🔍 Consultar reservas':
    st.subheader('Reservas registradas')

    estado = st.selectbox('Filtrar por estado', ['ACTIVA', 'FINALIZADA', 'CANCELADA'])

    filtradas = consultar(f"""
        select
            r.reserva_id,
            h.nombre,
            hab.num_habitacion,
            r.fecha_ingreso,
            r.fecha_salida,
            r.monto_total,
            r.estado
        from ht_reservas r
        join ht_huespedes h on r.huesped_id = h.huesped_id
        join ht_habitaciones hab on r.habitacion_id = hab.habitacion_id
        where r.estado = '{estado}'
        order by r.reserva_id
    """)

    st.write(f'Reservas encontradas: **{len(filtradas)}**')

    st.dataframe(
        filtradas.rename(columns={
            'reserva_id': 'ID',
            'nombre': 'Huésped',
            'num_habitacion': 'Habitación',
            'fecha_ingreso': 'Ingreso',
            'fecha_salida': 'Salida',
            'monto_total': 'Total',
            'estado': 'Estado'
        }),
        use_container_width=True,
        hide_index=True
    )

#------------------CONSULTAR RESERVAS-------------------
elif pagina == "🔍 Consultar reservas":
    st.subheader("🔍 Reservas registradas")

    estado = st.selectbox("Filtrar por estado", ["ACTIVA" , "FINALIZADA" , "CANCELADA"])

    filtradas = consultar(f"""
    SELECT r.reserva_id, h.nombre, hab.num_habitacion, r.fecha_ingreso, r.fecha_salida, r.monto_total, r.estado
    FROM ht_reservas r
    JOIN ht_huespedes h ON r.huesped_id = h.huesped_id
    JOIN ht_habitaciones hab ON r.habitacion_id = hab.habitacion_id
    WHERE r.estado = '{estado}'
    ORDER BY r.fecha_ingreso DESC
""")

    st.write(f"Reservas encontradas: **{len(filtradas)}**")

    st.dataframe(filtradas.
                 rename(columns = {"reserva_id": "ID",
                                   "nombre": "Huésped",
                                   "num_habitacion": "Habitación",
                                   "fecha_entrada": "Entrada",
                                   "fecha_salida": "Salida",
                                   "monto_final": "Total",
                                   "estado": "Estado"}),
                 use_container_width=True,
                 hide_index=True)

#---------------REGISTRAR NUEVA RESERVA-----------------
elif pagina == "📆 Registrar nueva reserva":
    st.subheader("📆 Nueva reserva")
    # Opciones de habitaciones disponibles para registrar

    disponibles = consultar("""
    SELECT  habitacion_id, num_habitacion || '-'
    || tipo || '($' || precio_noche || ')' AS etiqueta, precio_noche
    FROM ht_habitaciones
    WHERE estado = 'DISPONIBLE' 
""")

    opciones_hab = disponibles["ETIQUETA"].tolist()

    col_3, col_4 = st.columns(2)
    with col_3:
        num_doc = st.text_input("Numero de documento del huesped")
        habitacion = st.selectbox("Habitacion" , opciones_hab)
        fecha_entrada = st.date_input("Fecha de entrada", value = date.today())
        email = st.text_input("Correo electronico")

    with col_4:
        nombre = st.text_input("Nombre completo del huesped")
        canal = st.selectbox("Canal", ["TRANSFERENCIA", "PSE", "TC"])
        fecha_salida = st.date_input("Fecha de salida", value = date.today())

        #Calcular el total estimado
        hab_seleccionada = disponibles[disponibles["ETIQUETA"] == habitacion]
        if not hab_seleccionada.empty:
            precio = int(hab_seleccionada["PRECIO_NOCHE"].values[0])
            noches = (fecha_salida - fecha_entrada).days
            #Para evitar valores negativos
            noches = max(noches, 0)
            st.info(f"{noches} noches x \${precio} = \${noches*precio: ,}")
            if st.button("Registrar reserva", type="primary"):
                if not num_doc or not nombre:
                    st.warning("Complete el nombre y el numero de documento")
                elif fecha_salida <= fecha_entrada:
                    st.warning("La fecha de salida debe ser mayor a la fecha de entrada")
                else:
                    try:
                        conn = conectar()
                        cursor = conn.cursor()

                        # - Si el huesped ya esta registrado en la base de datos
                        cursor.execute(
                            "SELECT huesped_id FROM ht_huespedes WHERE num_doc = :doc",
                            doc=num_doc
                        )
                        huesped_listados = cursor.fetchone()

                        # - Si no esta registrado, hacerlo
                        if huesped_listados is None:
                            cursor.execute("""
                                           INSERT INTO ht_huespedes (tipo_doc, num_doc, nombre, email, estado)
                                           VALUES ('CC', :doc, :nombre, :email, 'ACTIVO')
                                           """,
                                           doc=num_doc,
                                           nombre=nombre,
                                           email=email if email else None
                                           )
                            cursor.execute(
                                "SELECT huesped_id FROM ht_huespedes WHERE num_doc = :doc",
                                doc=num_doc
                            )
                            huesped_listados = cursor.fetchone()

                        huesped_id = huesped_listados[0]

                        # 3. cruzar el id de la habitacion con la reserva
                        cursor.execute(
                            "SELECT habitacion_id FROM ht_habitaciones WHERE num_habitacion = :num_hab",
                            num_hab=habitacion.split('-')[0]
                        )
                        hab_listadas = cursor.fetchone()
                        habitacion_id = hab_listadas[0]

                        # 4. Registrar el huesped en la tabla de reservas
                        cursor.execute("""
                                       INSERT INTO ht_reservas (huesped_id, habitacion_id, fecha_ingreso, fecha_salida,
                                                                monto_total, estado)
                                       VALUES (:huesped_id, :habitacion_id, :fecha_entrada, :fecha_salida, :monto, 'ACTIVA')
                                       """,
                                       huesped_id=huesped_id,
                                       habitacion_id=habitacion_id,
                                       fecha_ingreso=fecha_entrada,
                                       fecha_salida=fecha_salida,
                                       monto=noches * precio
                                       )

                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.success(
                            f'Reserva registrada a nombre de {nombre} '
                            f'por {noches} noches por un valor total de ${noches * precio:,}'
                        )

                    except Exception as error:
                        st.error(f'Error al registrar la reserva: {error}')

# ----------- 4. REGISTRAR PAGO ---------------------------

elif pagina == '💵 Registrar pago':
    st.subheader('💵 Registrar pago')

    reservas_con_saldo = consultar("""
                                   select r.reserva_id,
                                          h.nombre,
                                          hab.num_habitacion,
                                          r.monto_total - NVL(sum(p.monto_pago), 0) as saldo_pendiente
                                   from ht_reservas r
                                            join ht_huespedes h on h.huesped_id = r.huesped_id
                                            join ht_habitaciones hab on r.habitacion_id = hab.habitacion_id
                                            left join ht_pagos p on r.reserva_id = p.reserva_id
                                   where r.estado = 'ACTIVA'
                                   group by r.reserva_id, h.nombre, hab.num_habitacion, r.monto_total
                                   having r.monto_total - NVL(SUM(p.monto_pago), 0) > 0
                                   """)

    if reservas_con_saldo.empty:
        st.info('No hay reservas con saldo pendiente')
    else:
        etiquetas = (
                reservas_con_saldo["NOMBRE"]
                + " — Hab. "
                + reservas_con_saldo["NUM_HABITACION"].astype(str)
        )

        reserva_sel = st.selectbox("Reserva", etiquetas.tolist())

        fila = reservas_con_saldo[etiquetas == reserva_sel].iloc[0]
        saldo = float(fila["SALDO_PENDIENTE"])

        st.write(f"Saldo pendiente: **${saldo:,.0f}**")

        col_1, col_2 = st.columns(2)
        with col_1:
            monto = st.number_input(
                "Monto del pago ($)",
                min_value=1000.0,
                max_value=saldo,
                value=saldo,
                step=10000.0
            )
        with col_2:
            medio = st.selectbox(
                "Medio de pago",
                ["EFECTIVO", "TARJETA_CREDITO", "TRANSFERENCIA", "PSE"]
            )

        if st.button("Registrar pago", type="primary"):
            # Registro con Oracle
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                           insert into ht_pagos (reserva_id, fecha_pago, monto_pago, canal_pago)
                           values (:reserva_id, TRUNC(SYSDATE), :monto, :canal)
                           """, {
                               'reserva_id': int(fila['RESERVA_ID']),
                               'monto': monto,
                               'canal': medio
                           })
            conn.commit()
            cursor.close()
            conn.close()

            st.success(f"Pago de ${monto:,.0f} registrado por {medio}.")