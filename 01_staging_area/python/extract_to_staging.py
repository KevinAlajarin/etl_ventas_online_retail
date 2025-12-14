import pandas as pd
import sqlalchemy
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

def extract_csv_to_raw():
    print(">>> [Extract] Leyendo CSV hacia Staging RAW...")
    
    if not os.path.exists(Config.RAW_DATA_PATH):
        raise FileNotFoundError(f"El archivo {Config.RAW_DATA_PATH} no existe.")

    # 1. Lectura del CSV
    df = pd.read_csv(Config.RAW_DATA_PATH, encoding='latin1', dtype=str)
    print(f"    Registros leídos del CSV: {len(df)}")
    
    # TRANSFORMACIÓN DE ESQUEMA
    print("    Normalizando columnas del CSV para coincidir con SQL...")
    
    rename_map = {
        'Invoice': 'InvoiceNo',
        'Price': 'UnitPrice',
        'Customer ID': 'CustomerID'
    }
    df.rename(columns=rename_map, inplace=True)
    
    expected_columns = [
        'InvoiceNo', 'StockCode', 'Description', 'Quantity', 
        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'
    ]
    
    # Nos quedamos solo con las columnas esperadas, ignoramos 'Year', 'Month', 'TotalPrice', etc.
    df_final = df[df.columns.intersection(expected_columns)].copy()
    
    # Ordenamos columnas para asegurar coincidencia
    for col in expected_columns:
        if col not in df_final.columns:
            df_final[col] = None
    
    df_final = df_final[expected_columns]
    # ---------------------------------------

    print(f"    Insertando {len(df_final)} filas con estructura corregida...")

    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    with engine.connect() as connection:
        print("    Truncando tabla raw...")
        connection.execute(sqlalchemy.text("TRUNCATE TABLE staging.raw_retail"))
        
        print("    Insertando en SQL Server...")
        df_final.to_sql('raw_retail', con=connection, schema='staging', if_exists='append', index=False, chunksize=1000)
        
        connection.commit() 
        print(">>> [Extract] Carga RAW completada y confirmada.")

if __name__ == "__main__":
    extract_csv_to_raw()