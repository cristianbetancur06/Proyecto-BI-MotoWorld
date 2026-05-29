# =========================================================
# IMPORTAMOS LAS LIBRERÍAS
# =========================================================
import streamlit as st
import pandas as pd
from datetime import date

from connection import conectar


# =========================================================
# CONEXIÓN A ORACLE
# =========================================================

def consultar(sql):
    conn = conectar()
    return pd.read_sql(sql, conn)

# =========================================================
# TÍTULO Y DESCRIPCIÓN
# =========================================================

st.set_page_config(page_title="MotoWorld 🏍️", layout="wide")
st.title("🏍️ MotoWorld")
st.write("Sistema de gestión de concesionario de motos")


# =========================================================
# MENÚ LATERAL
# =========================================================

st.sidebar.header("Menú")
pagina = st.sidebar.radio(
    "Seleccione una opción",
    [
        "🏍️ Motos disponibles",
        "🔍 Consultar compras",
        "🛒 Registrar compra",
        "💵 Registrar pago"
    ]
)

col_1, col_2 = st.columns(2)
with col_1:
    st.write("Sistema de gestión de motos e inventario")
with col_2:
    st.write(f"Sección activa: **{pagina}**")

st.divider()


# =========================================================
# 1. MOTOS DISPONIBLES
# =========================================================

if pagina == "🏍️ Motos disponibles":
    st.subheader("🏍️ Catálogo de Motos Disponibles")

#-----Traemos las motos que tengan como estado diponible
    motos = consultar("""
        SELECT
            moto_id,
            placa,
            marca,
            modelo,
            año_fabricacion,
            cilindraje,
            color,
            precio,
            estado
        FROM mt_motos
        WHERE estado = 'DISPONIBLE'
        ORDER BY marca, año_fabricacion DESC
        """)

    if motos.empty:
        st.warning("No hay motos disponibles en este momento.")
    else:

#--------Filtramos por marca y año
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            marcas = ["- Seleccione una marca -"] + sorted(motos["MARCA"].unique().tolist())
            marca_sel = st.selectbox("🔎 Seleccione una marca", marcas)

        with col_f2:
            años = ["Todos"] + sorted(motos["AÑO_FABRICACION"].unique().tolist(), reverse=True)
            año_sel = st.selectbox("📅 Filtrar por año", años)

#-------No mostrar nada sino elije una marca
        if marca_sel == "- Seleccione una marca -":
            st.info("Seleccione una marca para ver las motos disponibles.")

        else:
#--------Filtrar por marca
            filtradas = motos[motos["MARCA"] == marca_sel].copy()

#--------Filtrar por año
            if año_sel != "Todos":
                filtradas = filtradas[filtradas["AÑO_FABRICACION"] == año_sel]

#--------Contador
            st.write(f"Motos disponibles: **{len(filtradas)}**")
            st.divider()

#------Tarjetas
            if filtradas.empty:
                st.info("No hay motos que coincidan con los filtros seleccionados.")

            else:
                cols_por_fila = 3
                filas = [filtradas.iloc[i:i+cols_por_fila] for i in range(0, len(filtradas), cols_por_fila)]

                for fila in filas:
                    cols = st.columns(cols_por_fila)
                    for idx, (_, moto) in enumerate(fila.iterrows()):
                        with cols[idx]:
                            st.write(f"**{moto['MARCA']} — {moto['MODELO']}**")
                            st.write(f"💰 Precio: **${int(moto['PRECIO']):,}**")
                            st.write(f"🔩 Cilindraje: {int(moto['CILINDRAJE'])} cc")
                            st.write(f"📅 Año: {int(moto['AÑO_FABRICACION'])}")
                            st.write(f"🎨 Color: {moto['COLOR']}")
                            st.write(f"🪪 Placa: {moto['PLACA']}")
                            st.divider()



# =========================================================
# 2. CONSULTAR COMPRAS
# =========================================================

elif pagina == "🔍 Consultar compras":
    st.subheader("🔍 Compras registradas")

    estado = st.selectbox("Filtrar por estado", ["ACTIVA", "CANCELADA", "PAGO"])

#-----Traemos las compras que tengan los 3 estados posibles
    compras = consultar(f"""
        SELECT
            c.compra_id,
            cl.nombre,
            m.marca,
            m.modelo,
            m.placa,
            c.fecha_compra,
            c.monto_total,
            c.tipo_venta,
            c.estado
        FROM mt_compras c
        JOIN mt_clientes cl
            ON c.cliente_id = cl.cliente_id
        JOIN mt_motos m
            ON c.moto_id = m.moto_id
        WHERE c.estado = '{estado}'
        ORDER BY c.fecha_compra DESC
    """)


#----Validar resultados
    if compras.empty:
        st.warning("No existen compras registradas con ese estado.")
    else:
        compras["FECHA_COMPRA"] = pd.to_datetime(compras["FECHA_COMPRA"]).dt.strftime("%d/%m/%Y")
        st.write(f"Compras encontradas: **{len(compras)}**")
        st.divider()

#--------Tabla
        st.dataframe(
            compras.rename(columns={
                "COMPRA_ID": "ID Compra",
                "NOMBRE": "Cliente",
                "MARCA": "Marca",
                "MODELO": "Modelo",
                "PLACA": "Placa",
                "FECHA_COMPRA": "Fecha Compra",
                "MONTO_TOTAL": "Monto Total",
                "TIPO_VENTA": "Tipo Venta",
                "ESTADO": "Estado"
            }),
        use_container_width=True,
        hide_index=True
    )



# =========================================================
# 3. REGISTRAR COMPRA
# =========================================================

elif pagina == "🛒 Registrar compra":
    st.subheader("🛒 Registrar Nueva Compra")

# ----Traemos las motos disponibles con etiqueta para el selectbox
    disponibles = consultar("""
                            SELECT moto_id,
                                placa || ' - ' || marca || ' ' || modelo || ' ($' || precio || ')' AS etiqueta,
                                precio
                            FROM mt_motos
                            WHERE estado = 'DISPONIBLE'
                            ORDER BY marca, modelo
                            """)

    if disponibles.empty:
        st.warning("No hay motos disponibles para la venta en este momento.")

    else:
        opciones_moto = ["— Seleccione una moto —"] + disponibles["ETIQUETA"].tolist()

        col_3, col_4 = st.columns(2)

#------Establecemos el contenido que va a tener las columnas de este apartado
        with col_3:
            nombre = st.text_input("Nombre completo del cliente")
            tipo_doc = st.selectbox("Tipo de documento", ["CC", "CE", "NIT", "PP"])
            num_doc = st.text_input("Número de documento del cliente")
            email = st.text_input("Correo electrónico")

        with col_4:
            telefono = st.text_input("Teléfono")
            moto_sel = st.selectbox("Moto", opciones_moto)
            tipo_venta = st.selectbox("Tipo de venta", ["CONTADO", "FINANCIADO"])
            fecha_compra = st.date_input("Fecha de compra", value=date.today())

#-------Obtener precio de la moto seleccionada
        if moto_sel != "— Seleccione una moto —":
            moto_fila = disponibles[disponibles["ETIQUETA"] == moto_sel]
            precio = int(moto_fila["PRECIO"].values[0])
            st.info(f"💰 Monto total de la compra: **${precio:,}**")

#-------Botón que permite registrar las compras
            if st.button("Registrar compra", type="primary"):
                if not num_doc or not nombre:
                    st.warning("Complete el nombre y el número de documento")
                else:
                    try:
                        conn = conectar()
                        cursor = conn.cursor()

                # 1. Buscar si el cliente ya existe
                        cursor.execute(
                    "SELECT cliente_id FROM mt_clientes WHERE num_doc = :doc",
                        doc=num_doc
                        )
                        cliente = cursor.fetchone()

                # 2. Si no existe, crearlo
                        if cliente is None:
                            cursor.execute("""
                                    INSERT INTO mt_clientes (tipo_doc, num_doc, nombre, telefono, email, estado)
                                    VALUES (:tipo_doc, :doc, :nombre, :telefono, :email, 'ACTIVO')
                                    """,
                                    tipo_doc=tipo_doc,
                                    doc=num_doc,
                                    nombre=nombre,
                                    telefono=telefono if telefono else None,
                                    email=email if email else None
                                    )
                            cursor.execute(
                        "SELECT cliente_id FROM mt_clientes WHERE num_doc = :doc",
                                doc=num_doc
                            )
                            cliente_lis = cursor.fetchone()
                        else:
                            cliente_lis = cliente

                        cliente_id = cliente_lis[0]

                # 3. Obtener moto_id
                        cursor.execute(
                            "SELECT moto_id FROM mt_motos WHERE placa = :placa",
                            placa=moto_sel.split(" - ")[0]
                        )
                        moto_lis = cursor.fetchone()
                        moto_id  = moto_lis[0]


                # 4. Insertar la compra
                        cursor.execute("""
                            INSERT INTO mt_compras (cliente_id, moto_id, fecha_compra, monto_total, tipo_venta, estado)
                            VALUES (:cliente_id, :moto_id, :fecha_compra, :monto, :tipo_venta, 'ACTIVA')
                            """,
                                cliente_id=cliente_id,
                                moto_id=moto_id,
                                   fecha_compra=fecha_compra,
                                monto=precio,
                                tipo_venta=tipo_venta
                        )
                # 5. Cambiar el estado de la moto a VENDIDA
                        cursor.execute("""
                            UPDATE mt_motos
                            SET estado = 'VENDIDA'
                            WHERE moto_id = :moto_id
                            """, moto_id=moto_id)

                        conn.commit()
                        cursor.close()
                        conn.close()

#---------------La etiqueta que se mostrará al momento de registrar la compra
                        st.success(
                            f"Compra registrada exitosamente a nombre de **{nombre}** — "
                            f"**{moto_sel.split(' - ')[1].split(' ($')[0]}** "
                            f"por un valor de **${precio:,}** en modalidad **{tipo_venta}**."
                        )

                    except Exception as error:
                        st.error(f"Error al registrar la compra: {error}")


# =========================================================
# 4. REGISTRAR PAGO
# =========================================================

elif pagina == "💵 Registrar pago":
    st.subheader("💵 Registrar Pago")

#------Traer compras ACTIVAS con saldo pendiente
    compras_con_saldo = consultar("""
        SELECT 
            c.compra_id,
            cl.nombre,
            m.marca || ' ' || m.modelo AS moto,
            m.placa,
            c.monto_total,
            c.tipo_venta,
            c.fecha_compra,
            (c.monto_total - NVL(SUM(p.monto_pago), 0)) AS saldo_pendiente
        FROM mt_compras c
        JOIN mt_clientes cl ON cl.cliente_id = c.cliente_id
        JOIN mt_motos m ON m.moto_id = c.moto_id
        LEFT JOIN mt_pagos p ON p.compra_id = c.compra_id
        WHERE c.estado = 'ACTIVA'
        GROUP BY c.compra_id, cl.nombre, m.marca, m.modelo, m.placa, c.monto_total, c.tipo_venta, fecha_compra
        HAVING (c.monto_total - NVL(SUM(p.monto_pago), 0)) > 0
""")
    if compras_con_saldo.empty:
        st.info("No hay compras con saldo pendiente")
    else:
#-------Etiqueta: Nombre cliente — Marca Modelo (Placa)
        etiquetas = (compras_con_saldo["NOMBRE"] + " — " + compras_con_saldo["MOTO"] + " ( " + compras_con_saldo["PLACA"]  + ")"
        )

#-------Lista con la etiqueta creada
        compra_sel = st.selectbox("Seleccione la compra", etiquetas.tolist())

        fila = compras_con_saldo[etiquetas == compra_sel].iloc[0]
        saldo = float(fila["SALDO_PENDIENTE"])

#-------Organización de lo que va a contener las columnas de este apartado
        col_1, col_2 = st.columns(2)
        with col_1:
            st.write(f"Tipo de venta: **{fila['TIPO_VENTA']}**")
            st.write(f"Monto total: **${float(fila['MONTO_TOTAL']):,.0f}**")
            st.write(f"Saldo pendiente: **${saldo:,.0f}**")
        with col_2:
            monto = st.number_input("Monto del pago ($)", min_value=1000.0, max_value=saldo, value=saldo, step=10000.0)
            medio = st.selectbox("Canal de pago", ["EFECTIVO", "TRANSFERENCIA", "TC", "PSE"])

#------Botón para registar el pago
        if st.button("Registrar pago", type="primary"):
            # Realizamos la conexión con SQL para registrar los datos insertados por los clientes relacionados a los pagos
            try:
                conn = conectar()
                cursor = conn.cursor()

            # Generar referencia automática

                prefijos = {
                 "TRANSFERENCIA": "TF",
                 "PSE": "PSE",
                 "TC": "TC",
                 "EFECTIVO": "EF"
                }

                pre = prefijos.get(medio, "PG")

            # Contar pagos existentes con ese canal para el consecutivo
                cursor.execute("""
                        SELECT COUNT(*)
                        FROM mt_pagos
                        WHERE canal_pago = :canal
                        """, canal=medio)

                consecutivo = cursor.fetchone()[0] + 1
                referencia = f"{pre}-{consecutivo:03}"

            # Insertar el pago
                cursor.execute("""
                           INSERT INTO mt_pagos (compra_id, fecha_pago, monto_pago, canal_pago, referencia)
                            VALUES (:compra_id, TRUNC(SYSDATE), :monto, :canal, :referencia)
                           """, {
                               'compra_id': int(fila['COMPRA_ID']),
                               'monto': monto,
                               'canal': medio,
                               'referencia': referencia
                           })

                # Si el saldo queda en 0 con este pago, cerrar la compra
                if monto >= saldo:
                    cursor.execute("""
                                    UPDATE mt_compras
                                    SET estado = 'PAGO'
                                    WHERE compra_id = :compra_id
                                """, compra_id=int(fila['COMPRA_ID']))

                conn.commit()
                cursor.close()
                conn.close()

                # Etiqueta de lo se mostrará si el cliente paga todo el saldo
                if monto >= saldo:
                    st.success(
                        f"Pago de **${monto:,.0f}** registrado por **{medio}** "
                        f"con referencia **{referencia}**. "
                        f"¡Compra saldada completamente!"
                    )
                else:
                # Etiqueta de lo se mostrará si el cliente queda con saldo pendiente
                    nuevo_saldo = saldo - monto
                    st.success(
                        f"Pago de ${monto:,.0f} registrado por {medio} "
                        f"con referencia {referencia}. "
                        f"Saldo restante: ${nuevo_saldo:,.0f}"
                    )
            except Exception as error:
                st.error(f"Error al registrar el pago: {error}")