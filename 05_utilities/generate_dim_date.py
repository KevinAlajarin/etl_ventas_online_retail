import pandas as pd
import sqlalchemy
import sys
import os
from sqlalchemy import text

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', '01_staging_area', 'python')
sys.path.append(config_path)

from config import Config

def populate_dim_date(start='2009-01-01', end='2025-12-31'):
    print(">>> [Generador] Creando dataframe de fechas en memoria...")
    dates = pd.date_range(start=start, end=end)
    df = pd.DataFrame({'full_date': dates})
    
    # Transformaciones
    df['date_key'] = df['full_date'].dt.strftime('%Y%m%d').astype(int)
    df['year'] = df['full_date'].dt.year
    df['quarter'] = df['full_date'].dt.quarter
    df['month_num'] = df['full_date'].dt.month
    df['month_name'] = df['full_date'].dt.month_name()
    df['day_of_week'] = df['full_date'].dt.dayofweek + 1
    df['day_name'] = df['full_date'].dt.day_name()
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 6 else 0)
    
    print(f">>> [Base de Datos] Conectando a {Config.DB_SERVER}...")
    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    # Usamos connect() y hacemos commit
    with engine.connect() as connection:
        # 1. Verificar si ya existe data
        count = connection.execute(text("SELECT COUNT(*) FROM dw.DimDate")).scalar()
        if count > 0:
            print(f"!!! La tabla DimDate ya tiene {count} registros. Omitiendo carga.")
            return

        print(f">>> [Insertando] Escribiendo {len(df)} filas en SQL Server...")
        
        # 2. Insercion
        df.to_sql('DimDate', con=connection, schema='dw', if_exists='append', index=False, chunksize=1000)
        
        # 3. Confirmar la transaccion
        connection.commit()
        print(">>> [Éxito] Commit realizado. Datos guardados permanentemente.")

if __name__ == "__main__":
    populate_dim_date()