import sys
import os
import sqlalchemy
from sqlalchemy import text

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', '..', '01_staging_area', 'python')
sys.path.append(config_path)

from config import Config

def run_quality_checks():
    print(f">>> [Quality Control] Conectando a {Config.DB_NAME}...")
    engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DB_URI)
    
    # Diccionario de reglas: Nombre -> Query SQL
    # Las queries deben retornar count(*) de registros FALLIDOS (Malos)
    checks = {
        # Ventas con productos que no existen en DimProduct
        "Orphan Products": """
            SELECT COUNT(*) 
            FROM dw.FactSales f 
            LEFT JOIN dw.DimProduct p ON f.product_key = p.product_key 
            WHERE p.product_key IS NULL
        """,
        
        # Precios negativos o cero (que no sean devoluciones)
        "Invalid Prices": "SELECT COUNT(*) FROM dw.FactSales WHERE unit_price <= 0 AND is_return = 0",
        
        # Ventas sin fecha asignada
        "Null Dates": "SELECT COUNT(*) FROM dw.FactSales WHERE date_key IS NULL",
        
        # Integridad de Clientes
        "Orphan Customers": """
            SELECT COUNT(*) 
            FROM dw.FactSales f 
            LEFT JOIN dw.DimCustomer c ON f.customer_key = c.customer_key 
            WHERE c.customer_key IS NULL
        """
    }
    
    all_passed = True
    
    with engine.connect() as conn:
        print(">>> Ejecutando batería de pruebas...")
        for name, query in checks.items():
            try:
                result = conn.execute(text(query)).scalar()
                
                if result == 0:
                    status = "[PASS] ✅"
                else:
                    status = f"[FAIL] ❌ ({result} registros fallidos)"
                    all_passed = False
                
                print(f"    {status} {name}")
                
            except Exception as e:
                print(f"    [ERROR] ⚠️ Falló la ejecución de '{name}': {e}")
                all_passed = False

    print("-" * 30)
    if all_passed:
        print(">>> RESULTADO FINAL: APROBADO. El Data Warehouse es íntegro.")
    else:
        print(">>> RESULTADO FINAL: FALLIDO. Revisar reglas de limpieza.")

if __name__ == "__main__":
    run_quality_checks()