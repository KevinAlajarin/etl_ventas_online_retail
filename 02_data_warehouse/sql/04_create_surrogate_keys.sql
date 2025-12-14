/*
DOCUMENTACIÓN TeCNICA 

Estrategia de Generación:
Se utiliza la propiedad IDENTITY(1,1) nativa de SQL Server directamente en los scripts DDL
(02_create_dimensions.sql y 03_create_fact_table.sql).

Mapeo:
- dw.DimProduct.product_key  -> INT IDENTITY(1,1)
- dw.DimCustomer.customer_key -> INT IDENTITY(1,1)
- dw.DimCountry.country_key  -> INT IDENTITY(1,1)
- dw.FactSales.fact_sales_key -> BIGINT IDENTITY(1,1)

*/