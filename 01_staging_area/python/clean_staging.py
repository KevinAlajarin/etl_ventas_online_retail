import pandas as pd
import sqlalchemy
import numpy as np
from config import Config

def clean_and_load_staging():
    print(">>> Iniciando limpieza y transformación hacia Staging CLEAN...")
    
    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    # 1. Leer RAW
    query = "SELECT * FROM staging.raw_retail"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("    Staging RAW está vacío. Nada que procesar.")
        return

    # Conversion de Tipos inicial
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0.0)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    initial_count = len(df)

    # 2. Aplicar Reglas de Calidad 
    
    # DQ_01: Eliminar Cancelaciones 
    df = df[~df['InvoiceNo'].str.startswith('C', na=False)]
    
    # DQ_02: Eliminar Precios <= 0
    df = df[df['UnitPrice'] > 0]

    # DQ_03: Logica IsReturn
    df['IsReturn'] = df['Quantity'] < 0

    # DQ_04: CustomerID Nulo -> -1
    df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce').fillna(-1).astype('int64')

    # DQ_05: Descripciones Vacias
    df['Description'] = df['Description'].fillna('No Description')
    
    # DQ_06: Eliminar Duplicados Exactos
    df = df.drop_duplicates()
        
    # Calculo LineTotal
    df['LineTotal'] = df['Quantity'] * df['UnitPrice']
    
    final_count = len(df)
    print(f"    Filas iniciales: {initial_count} -> Filas limpias: {final_count} (Eliminadas: {initial_count - final_count})")

# 3. Carga a Staging Clean
    with engine.connect() as connection:
        print("    Limpiando tabla staging.clean_retail...")
        connection.execute(sqlalchemy.text("TRUNCATE TABLE staging.clean_retail"))
        
        print(f"    Insertando {len(df)} filas limpias...")
        df.to_sql('clean_retail', con=connection, schema='staging', if_exists='append', index=False, chunksize=1000)
        
        connection.commit()

    print(">>> [Transform] Staging CLEAN cargada y confirmada.")

if __name__ == "__main__":
    clean_and_load_staging()