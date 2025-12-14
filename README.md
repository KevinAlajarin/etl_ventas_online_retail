# 🛒 Retail Sales Data Warehouse (End-to-End)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2019%2B-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)
![ETL](https://img.shields.io/badge/ETL-Incremental-4B8BBE?style=for-the-badge)

Un proyecto de ingeniería de datos completo que implementa un Data Warehouse moderno para una empresa de Retail. El sistema ingesta datos transaccionales, los normaliza en un modelo **Estrella (Star Schema)** y presenta insights de negocio a través de un dashboard interactivo.

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue una arquitectura ELT/ETL robusta diseñada para ser escalable e incremental.

```mermaid
graph LR
    A[CSV Source] -->|Extract| B(Staging Area - Python);
    B -->|Transform & Clean| C{SQL Server Staging};
    C -->|Load (SP Incremental)| D[(Data Warehouse - Star Schema)];
    D -->|Semantic Layer| E[SQL Views];
    E -->|Visualize| F[Power BI Dashboard];
Componentes Clave
Ingesta & Limpieza (Python): Scripts modulares (pandas, sqlalchemy) que normalizan esquemas y aplican reglas de calidad (eliminación de devoluciones, manejo de nulos).

Staging Area (SQL): Tablas intermedias (raw y clean) para desacoplar la extracción de la carga.

Data Warehouse (SQL Server):

Modelo Estrella: Fact Table central (FactSales) rodeada de Dimensiones (DimProduct, DimCustomer, DimDate, DimCountry).

Carga Incremental: Stored Procedure inteligente que gestiona Upserts (SCD Tipo 1) y marcas de agua (Watermarks) para cargar solo datos nuevos.

Analytics: Vistas SQL materializadas para métricas pre-calculadas y Dashboard en Power BI con medidas DAX.

📂 Estructura del Proyecto
Plaintext

retail_data_warehouse/
├── 00_documentacion/      # Diagramas ERD, reglas de negocio y decisiones de diseño
├── 01_staging_area/       # Scripts Python para Ingesta y SQL para tablas temporales
├── 02_data_warehouse/     # DDLs del DW, Stored Procedures y Orquestador ETL
├── 03_analytical_layer/   # Vistas SQL para consumo de BI
├── 04_bi_powerbi/         # Archivo .pbix y guías de visualización
├── 05_utilities/          # Herramientas (Generador de DimDate, Reset)
└── requirements.txt       # Dependencias
```

🚀 Instrucciones de Ejecución
Prerrequisitos
Python 3.9+

SQL Server (Developer/Express)

Power BI Desktop

Paso 1: Configuración
Clonar el repositorio:

Bash

git clone [https://github.com/TU_USUARIO/retail_data_warehouse.git](https://github.com/TU_USUARIO/retail_data_warehouse.git)
cd retail_data_warehouse
Crear entorno virtual e instalar dependencias:

Bash

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configurar variables de entorno:

Renombrar .env.example a .env.

Editar .env con tus credenciales de SQL Server (DB_SERVER, DB_USER, etc.).

Paso 2: Base de Datos
Ejecutar los scripts SQL en SSMS en el siguiente orden estricto:

02_data_warehouse/sql/01_create_dw_database.sql

01_staging_area/sql/01_create_staging.sql

02_data_warehouse/sql/02_create_dimensions.sql

02_data_warehouse/sql/03_create_fact_table.sql

02_data_warehouse/sql/05_load_dimensions.sql (Carga miembros 'Unknown')

02_data_warehouse/sql/06_load_fact_incremental.sql (Stored Procedure)

Paso 3: Carga de Datos (ETL)
Colocar el dataset retail_cleans.csv en 01_staging_area/raw/.

Generar la Dimensión de Tiempo:

Bash

python 05_utilities/generate_dim_date.py
Ejecutar el Pipeline Maestro:

Bash

python 02_data_warehouse/python/etl_incremental.py
Este script orquesta la extracción, limpieza y carga incremental.

📊 Dashboard Overview
El reporte incluye:

KPIs Ejecutivos: Revenue, AOV, Total Orders.
Análisis Temporal: Tendencias de venta mensual/anual.
Top Products: Ranking de productos por ingresos (Pareto).
Geo-Spatial: Mapa de distribución de ventas por país.

Autor: Kevin Alajarin
