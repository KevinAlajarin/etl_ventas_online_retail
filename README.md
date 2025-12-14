# Retail Sales Data Warehouse Project

Implementación de referencia de un DW Retail con modelo estrella, ETL incremental en Python/SQL y capa analítica.

## Requisitos Previos
1. SQL Server Express/Developer instalado.
2. Python 3.9+.
3. Dataset de Kaggle descargado en `01_staging_area/raw/Online_Retail.csv`.

## Instrucciones de Ejecución (Paso a Paso)

1. **Configuración de Entorno:**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Editar .env con tus credenciales SQL