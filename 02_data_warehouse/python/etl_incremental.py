import sys
import os
import sqlalchemy
from sqlalchemy import text

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '01_staging_area', 'python'))

from config import Config
from extract_to_staging import extract_csv_to_raw
from clean_staging import clean_and_load_staging
from control_table import init_control_table

def run_etl():
    print(">>> [ETL MASTER] Iniciando proceso ETL Incremental Retail DW...")
    
    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    # 0. Check Conectividad y Control Table
    init_control_table(engine)
    
    # 1. Staging: Extraer 
    extract_csv_to_raw()
    
    # 2. Staging: Transformar
    clean_and_load_staging()
    
    # 3. DW: Cargar
    print(">>> Ejecutando Stored Procedure dw.sp_load_fact_incremental...")
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(text("EXEC dw.sp_load_fact_incremental"))
            trans.commit()
            print(">>> Carga al DW completada exitosamente.")
        except Exception as e:
            trans.rollback()
            print(f"!!! Error Crítico en Carga DW: {e}")
            raise e

    print(">>> [ETL MASTER] Proceso Finalizado.")

if __name__ == "__main__":
    run_etl()