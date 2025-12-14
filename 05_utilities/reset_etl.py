import sys
import os
import sqlalchemy
from sqlalchemy import text

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '01_staging_area', 'python'))
from config import Config

def hard_reset_dw():
    print("!!! ADVERTENCIA: INICIANDO RESET COMPLETO DEL DATA WAREHOUSE !!!")
    print("!!! ESTO BORRARÁ TODOS LOS DATOS EN STAGING Y DW !!!")
    confirm = input("Escribe 'DESTROY' para continuar: ")
    
    if confirm != 'DESTROY':
        print("Operación cancelada.")
        return

    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            print("1. Truncando Fact Table...")
            conn.execute(text("TRUNCATE TABLE dw.FactSales"))
            
            print("2. Reseteando Dimensiones (Conservando Unknowns)...")
            
            # DimProduct
            conn.execute(text("DELETE FROM dw.DimProduct WHERE product_key > 0"))
            
            # DimCustomer
            conn.execute(text("DELETE FROM dw.DimCustomer WHERE customer_key > 0"))
            
            # DimCountry
            conn.execute(text("DELETE FROM dw.DimCountry WHERE country_key > 0"))
            
            print("3. Limpiando Staging Area...")
            conn.execute(text("TRUNCATE TABLE staging.raw_retail"))
            conn.execute(text("TRUNCATE TABLE staging.clean_retail"))
            
            print("4. Reseteando Tabla de Control ETL...")
            conn.execute(text("UPDATE etl.control_table SET last_load_date = '2000-01-01' WHERE process_name = 'FactSales'"))
            
            trans.commit()
            print(">>> RESET COMPLETADO EXITOSAMENTE. El sistema está limpio.")
            
        except Exception as e:
            trans.rollback()
            print(f"!!! Error durante el reset: {e}")

if __name__ == "__main__":
    hard_reset_dw()