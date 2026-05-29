import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def conectar():

    oracledb.init_oracle_client(
        lib_dir=os.getenv("ORACLE_CLIENT")
    )

    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )