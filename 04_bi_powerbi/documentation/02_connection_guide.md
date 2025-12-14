# Guia de Conexion

1. Abrir Power BI Desktop.
2. `Get Data` -> `SQL Server`.
3. Server: `localhost` (o tu instancia). Database: `RetailDW`.
4. Data Connectivity Mode: `Import` (Recomendado para este volumen < 1GB).
5. Seleccionar tablas: `DimDate`, `DimProduct`, `DimCustomer`, `DimCountry`, `FactSales` O las Vistas Analíticas.
6. Cargar y Verificar Relaciones en la vista de Modelo.