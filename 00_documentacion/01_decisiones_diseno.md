# Decisiones de Diseño del Data Warehouse

## 1. Grano
* **Fact Table (FactSales):** 1 fila por línea de factura (Producto en una Transacción).
* **Identificación:** Combinación única de `InvoiceNo` + `StockCode`.

## 2. Modelo Dimensional (Star Schema)
* **FactSales:** Tabla central transaccional.
* **DimDate:** Dimensión de rol compartido (Role-playing) conectada a `InvoiceDate`.
* **DimProduct:** Dimensión SCD Tipo 1 (Sobrescribir cambios). `StockCode` es la Business Key.
* **DimCustomer:** Dimensión SCD Tipo 1. `CustomerID` es la Business Key. Manejo de nulos como 'Unknown'.
* **DimCountry:** Dimensión geográfica simple.

## 3. Estrategia ETL
* **Staging:** "Truncate and Load". Se cargan los datos crudos, se limpian en Python/Pandas y se vuelcan a `staging_clean`.
* **Incremental:** Basado en `InvoiceDate`.
    * Se consulta la tabla `etl_control` para obtener `last_high_watermark`.
    * Se procesan registros donde `InvoiceDate > last_high_watermark`.
    * **Idempotencia:** El Stored Procedure de carga utiliza lógica `MERGE` (o Left Join checks) para evitar duplicados si el proceso se re-ejecuta para el mismo rango.

## 4. Convenciones de Naming
* Tablas Fact: `Fact<Nombre>`
* Tablas Dim: `Dim<Nombre>`
* Surrogate Keys: `<nombre>_key` (Entero, IDENTITY)
* Business Keys: `<nombre>_id` o `code`