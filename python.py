import streamlit as st
import pandas as pd
import numpy as np
from datetime import date  # librería para gestionar fechas

# ----------- Datos de prueba -----------
# Estos datos tienen la misma estructura de la base de datos de oracle, pero
# serán manejados de forma temporal como dataframes
# ---------------------------------------------

df_habitaciones = pd.DataFrame({'habitacion_id': [1, 2, 3, 4, 5],
                                'num_habitacion': [101, 102, 201, 202, 301],
                                'tipo': ['SENCILLA', 'SENCILLA', 'DOBLE', 'DOBLE', 'SUITE'],
                                'precio_noche': [150000, 150000, 220000, 220000, 400000],
                                'estado': ['DISPONIBLE', 'OCUPADA', ' DISPONIBLE',
                                           'DISPONIBLE', 'DISPONIBLE']})

# Para la tabla de huéspedes
df_huespedes = pd.DataFrame({'huesped_id': [1, 2, 3],
                             'tipo_documento': ['CC', 'CE', 'Pasaporte'],
                             'num_documento': ['12345678', '87654321', 'AB123456'],
                             'nombre': ['Ana Torres', 'Luis Gómez', 'Marie Dupont'],
                             'estado': ['ACTIVO', 'ACTIVO', 'ACTIVO']})

# Para la tabla de reservas
df_reservas = pd.DataFrame({'reserva_id': [1, 2],
                            'huesped_id': [1, 2],
                            'habitacion_id': [1, 3],
                            'fecha_entrada': [date(2026, 4, 20), date(2026, 4, 22)],
                            'fecha_salida': [date(2026, 4, 25), date(2026, 4, 24)],
                            'monto_total': [750000, 440000],
                            'canal': ['DIRECTO', 'BOOKING'],
                            'estado': ['ACTIVA', 'ACTIVA']})

# Para la tabla de pagos
df_pagos = pd.DataFrame({'pago_id': [1],
                         'reserva_id': [1],
                         'fecha_pago': [date(2026, 4, 20)],
                         'monto_pago': [300000],
                         'medio_pago': ["EFECTIVO"]})

# -------- Títulos y Descripción ---------
st.set_page_config(page_title='BudAppest 🏩', layout='wide')
st.title('Hotel Budapest')
st.write('Esta aplicación gestiona el sistema de reservas del Hotel Budapest')

# ----------- Menú lateral ------------
st.sidebar.header('Menú')

pagina = st.sidebar.radio('Seleccione una opcion', ['🛌 Habitaciones disponibles',
                                                    '🔍 Consultar reservas',
                                                    '📅 Registrar nueva reserva',
                                                    '💵 Registrar pago'])

# Creamos dos columnas en la pantalla principal
col_1, col_2 = st.columns(2)

with col_1:
    st.write('Sistema de gestión de reservas BudApest')

with col_2:
    st.write(f'Sección activa: **{pagina}**')

st.divider()

# ----------- HABITACIONES DISPONIBLES ----
if pagina == '🛌 Habitaciones disponibles':
    st.subheader('🛌 Habitaciones disponibles')

    # Filtramos las habitaciones disponibles
    disponibles = df_habitaciones[df_habitaciones['estado'] == 'DISPONIBLE']

    # Mostramos la información relevante
    st.write(f'Total de habitaciones disponibles: **{len(disponibles)}**')

    # Ordenamos la informacion resultante de la consulta en una tabla
    st.dataframe(disponibles[['num_habitacion', 'tipo', 'precio_noche']].
    rename(columns={
        'num_habitacion': 'Número',
        'tipo': 'Tipo',
        'precio_noche': 'Precio por noche'}),
        use_container_width=True,
        hide_index=True)

# --------- CONSULTAR RESERVAS ----------

elif pagina == '🔍 Consultar reservas':
    st.subheader('Reservas registradas')

    estado = st.selectbox('Filtrar por estado', ['ACTIVA', 'FINALIZADA', 'CANCELADA'])

    # Filtrar las reservas por el estado y unir con huéspedes y habitaciones
    filtradas = df_reservas[df_reservas['estado'] == estado].copy()
    filtradas = filtradas.merge(df_huespedes[['huesped_id', 'nombre']],
                                on='huesped_id')
    filtradas = filtradas.merge(df_habitaciones[['habitacion_id',
                                                 'num_habitacion']],
                                on='habitacion_id')

    st.write(f'Reservas encontradas: **{len(filtradas)}**')

    st.dataframe(filtradas[["reserva_id", "nombre",
                            "num_habitacion", "fecha_entrada", "fecha_salida",
                            "monto_total", "estado"]].\
                 rename(columns= {
        "reserva_id": "ID",
        "nombre": "Huesped",
        "num_habitacion": "Habitación",
        "fecha_entrada": "Entrada",
        "fecha_salida": "Salida",
        "monto_total": "Total",
        "estado": "Estado"
    }),
        use_container_width=True,
        hide_index=True)
