import streamlit as st
import pandas as pd
import numpy as np
from datetime import date # Libreria para gestionar las fechas
import oracledb

#Creamos la funcion para conectar a la base de datos
@st.cache_resource
def conectar():
    oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_26")
    return oracledb.connect(
        user="cristian",  # reemplaza con tu usuario (ej: G07_E03)
        password="Cenicient4!!",  # reemplaza con tu contraseña de base de datos
        dsn="adbg07_low"  # reemplaza con tu servicio (ej: adbg07_low)
    )
#Creamos una funcion para ingresar las consultas en SQL
def consultar(sql):
    conn = conectar()
    return pd.read_sql(sql, conn)
