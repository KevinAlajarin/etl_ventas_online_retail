import sqlalchemy
from sqlalchemy import text

def init_control_table(engine):
    with engine.connect() as conn:
        conn.execute(text("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'etl') EXEC('CREATE SCHEMA [etl]')"))
        conn.commit()
        
        # Tabla simple clave-valor para fechas
        sql = """
        IF OBJECT_ID('etl.control_table', 'U') IS NULL
        CREATE TABLE etl.control_table (
            process_name VARCHAR(50) PRIMARY KEY,
            last_load_date DATETIME,
            updated_at DATETIME
        );
        """
        conn.execute(text(sql))
        conn.commit()
        
        # Inicializar si no existe
        conn.execute(text("""
            IF NOT EXISTS (SELECT 1 FROM etl.control_table WHERE process_name = 'FactSales')
            INSERT INTO etl.control_table (process_name, last_load_date, updated_at)
            VALUES ('FactSales', '2000-01-01', GETDATE());
        """))
        conn.commit()